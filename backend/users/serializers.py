from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import InternshipDocument, Student, AcademicSupervisor, WorkplaceSupervisor
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.db import transaction

User = get_user_model()

# ==========================================
# 1. PROFILE SERIALIZERS
# ==========================================

class StudentProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['registration_number', 'course']

class AcademicProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicSupervisor
        fields = ['department']

class WorkPlaceProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkplaceSupervisor  # FIXED: Added missing model mapping
        fields = ['organization_name']


# ==========================================
# 2. CORE USER SERIALIZER (Used by Admin Dashboard)
# ==========================================

class UserSerializer(serializers.ModelSerializer):
    # Dynamically fetched through reverse relations defined in your Models
    student_profile = StudentProfileSerializer(source='student', read_only=True)
    academic_profile = AcademicProfileSerializer(source="academicsupervisor", read_only=True)
    workplace_profile = WorkPlaceProfileSerializer(source='workplacesupervisor', read_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name', 
            'role', 'phone', 'is_active', 'date_joined', # ENHANCED: added is_active & date_joined for Admin analytics
            'student_profile', 'academic_profile', 'workplace_profile'
        ]


# ==========================================
# 3. JWT AUTHENTICATION SERIALIZER
# ==========================================

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['role'] = user.role  # Encrypted inside JWT payload
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        # Passed back in clear JSON text for React frontend router routing checks
        data['role'] = self.user.role
        data['username'] = self.user.username
        data['id'] = self.user.id
        return data


# ==========================================
# 4. REGISTRATION ENGINE
# ==========================================

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    
    # Make profile fields optional during base user registration step
    registration_number = serializers.CharField(required=False, allow_blank=True)
    course = serializers.CharField(required=False, allow_blank=True)
    department = serializers.CharField(required=False, allow_blank=True)
    organization_name = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = User
        fields = [
            'username', 'email', 'password', 'first_name', 'last_name', 
            'role', 'phone', 'registration_number', 'course', 'department', 'organization_name'
        ]

    def validate_registration_number(self, value):
        if value and Student.objects.filter(registration_number=value).exists():
            raise serializers.ValidationError("This registration number is already registered.")
        return value

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("This username is already taken.")
        return value

    def create(self, validated_data):
        with transaction.atomic():
            # Safely pop profile specific data out
            reg_no = validated_data.pop('registration_number', None)
            course = validated_data.pop('course', None)
            dept = validated_data.pop('department', None)
            org_name = validated_data.pop('organization_name', None)
            
            # Create core base user
            user = User.objects.create_user(**validated_data)

            # Route to correct model profile based on structural role selected
            if user.role == User.Role.STUDENT:
                Student.objects.create(user=user, registration_number=reg_no, course=course)
            elif user.role == User.Role.ACADEMIC_SUPERVISOR:
                AcademicSupervisor.objects.create(user=user, department=dept)
            elif user.role == User.Role.WORKPLACE_SUPERVISOR:
                WorkplaceSupervisor.objects.create(user=user, organization_name=org_name)
            
            return user


# ==========================================
# 5. INTERNSHIP DOCUMENT MANAGEMENT
# ==========================================

class InternshipDocumentSerializer(serializers.ModelSerializer):
    student_name = serializers.ReadOnlyField(source='student.get_full_name')

    class Meta:
        model = InternshipDocument
        fields = [
            'id', 'student', 'student_name', 'document_name', 
            'file', 'status', 'uploaded_at', 'remarks'
        ]
        # Admin views override read_only values when modifying status explicitly
        read_only_fields = ['student']