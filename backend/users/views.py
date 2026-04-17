from rest_framework import viewsets, status, permissions,generics
from rest_framework.permissions import AllowAny  # AllowAny lives here!
from rest_framework_simplejwt.tokens import RefreshToken # Add this import at the top
from .models import InternshipDocument
from rest_framework.response import Response # Fixed: should be Response, not responses
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model
from .serializers import (
    InternshipDocumentSerializer, 
    UserSerializer,
    MyTokenObtainPairSerializer,RegisterSerializer
)

# BUG FIX 1: get_user_model is a function and needs ()
User = get_user_model()


#register view 


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # FIX: Generate tokens directly here to avoid "AttributeError"
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


# --- Authentication views ---
class MyTokenObtainPairView(TokenObtainPairView):
    """
    Custom Login view that uses our custom serializer 
    to return the User Role to React.
    """
    serializer_class = MyTokenObtainPairSerializer

# --- User and profile views ---
class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    # BUG FIX 2: Use User.objects.all(), not User.objects().all
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == User.Role.ADMIN:
            return User.objects.all()
        return User.objects.filter(id=user.id)
    
# --- Document logic views ---   
class InternshipDocumentViewSet(viewsets.ModelViewSet):
    """
    Handles Document Uploads and Approval.
    """
    queryset = InternshipDocument.objects.all()
    serializer_class = InternshipDocumentSerializer
    # Ensure students must be logged in to upload
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        # 1. Students only see their own uploads
        if user.role == User.Role.STUDENT:
            return InternshipDocument.objects.filter(student=user)
        # 2. Supervisors see all documents for review
        elif user.role in [User.Role.ACADEMIC_SUPERVISOR, User.Role.WORKPLACE_SUPERVISOR]:
            return InternshipDocument.objects.all()
        
        return InternshipDocument.objects.none() # Safety fallback

    def perform_create(self, serializer):
        """
        Automatically assigns the logged-in user as the 'student'.
        """        
        serializer.save(student=self.request.user)
        print(f"Document Checker: New file uploaded by {self.request.user}")