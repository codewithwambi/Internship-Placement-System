from rest_framework import viewsets, status, permissions, generics, views
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model
from django.db.models import Count

from .models import InternshipDocument
from .serializers import (
    InternshipDocumentSerializer, 
    UserSerializer,
    MyTokenObtainPairSerializer, 
    RegisterSerializer
)

User = get_user_model()

# ==========================================
# CUSTOM PANEL PERMISSIONS
# ==========================================

class IsAdminUserRole(permissions.BasePermission):
    """Checks explicitly for the custom ADMIN role text field."""
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == User.Role.ADMIN


# ==========================================
# AUTHENTICATION & REGISTRATION VIEWS
# ==========================================

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        refresh = RefreshToken.for_user(user)
        tokens = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
        
        return Response({
            "user": UserSerializer(user).data,
            "tokens": tokens,
            "message": "User registered successfully."
        }, status=status.HTTP_201_CREATED)


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


# ==========================================
# USER PROFILE DIRECTORY ENDPOINT
# ==========================================

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed, updated, or deleted.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == User.Role.ADMIN:
            return User.objects.all().order_by('-id')
        return User.objects.filter(id=user.id)


# ==========================================
# DOCUMENT TRACKING & APPROVAL PIPELINE
# ==========================================

class InternshipDocumentViewSet(viewsets.ModelViewSet):
    """
    Handles Document Uploads, Review Remarks, and Approval workflows.
    """
    queryset = InternshipDocument.objects.all()
    serializer_class = InternshipDocumentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        
        # 1. Students can only see what they uploaded
        if user.role == User.Role.STUDENT:
            return InternshipDocument.objects.filter(student=user)
            
        # 2. Supervisors and Admins see everything across the system
        # FIXED: Added ADMIN to prevent the dashboard from returning empty files lists
        elif user.role in [User.Role.ACADEMIC_SUPERVISOR, User.Role.WORKPLACE_SUPERVISOR, User.Role.ADMIN]:
            return InternshipDocument.objects.all().order_by('-uploaded_at')
        
        return InternshipDocument.objects.none()

    def perform_create(self, serializer):
        serializer.save(student=self.request.user)

    def update(self, request, *args, **kwargs):
        """
        Interceptors to let Admin and Supervisors update status and append remarks.
        """
        instance = self.get_object()
        user = request.user

        if user.role == User.Role.STUDENT:
            return Response(
                {"detail": "Students are not allowed to update status fields or reviews."},
                status=status.HTTP_403_FORBIDDEN
            )
            
        # Partial updates via your dashboard buttons are cleanly extracted here
        instance.status = request.data.get('status', instance.status)
        instance.remarks = request.data.get('remarks', instance.remarks)
        instance.save()
        
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


# ==========================================
# DASHBOARD INSIGHTS ENGINE
# ==========================================

class AdminDashboardAnalyticsView(views.APIView):
    """
    Aggregates statistical database metrics for the front-end dashboard panels.
    """
    permission_classes = [IsAdminUserRole]

    def get(self, request):
        role_counts = User.objects.values('role').annotate(total=Count('role'))
        doc_counts = InternshipDocument.objects.values('status').annotate(total=Count('status'))
        
        payload = {
            "total_users": User.objects.count(),
            "roles": {item['role']: item['total'] for item in role_counts},
            "documents": {item['status']: item['total'] for item in doc_counts},
        }
        return Response(payload, status=status.HTTP_200_OK)