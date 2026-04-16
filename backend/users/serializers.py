from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import InternshipDocument,Student,AcademicSupervisor,WorkplaceSupervisor,User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer



#profile seriaizers

class  StudentProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=Student
        fields=['registration_number','course']

class AcademicProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=AcademicSupervisor
        fields=['department']

class WorkPlaceProfileSerializer(serializers.ModelSerializer):
    class Meta:
        fields=['organzation_name']

#user serializer

class UserSerializer(serializers.ModelSerializer):
    # these  will be populated based on user role
    student_profile=StudentProfileSerializer(source='student',read_only=True)
    academic_profile=AcademicProfileSerializer(source="academic supervisor",read_only=True)
    workplace_profile=WorkPlaceProfileSerializer(source='workplace supervisor',read_only=True)

    class Meta:
        model=User
        fields=[
            'id','username','email','first_name','last_name','role','phone',
            'student_profile','academic_profile','workplace_profile'
        ]


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = InternshipDocument
        fields = ['id', 'document_name', 'file', 'status', 'uploaded_at', 'remarks']
        read_only_fields = ['status', 'uploaded_at'] # Students can't approve their own docs!



class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add the role to the token payload (encrypted)
        token['role'] = user.role
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        # Add the role to the plain response (so React can see it immediately)
        data['role'] = self.user.role
        data['username'] = self.user.username
        return data
    
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Student, AcademicSupervisor, WorkplaceSupervisor, InternshipDocument
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()

# --- PROFILE SERIALIZERS ---

class StudentProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['registration_number', 'course']

class AcademicSupervisorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicSupervisor
        fields = ['department']

class WorkplaceSupervisorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkplaceSupervisor
        fields = ['organization_name']

# --- USER SERIALIZER ---

class UserSerializer(serializers.ModelSerializer):
    # These will be populated based on the user's role
    student_profile = StudentProfileSerializer(source='student', read_only=True)
    academic_profile = AcademicSupervisorProfileSerializer(source='academicsupervisor', read_only=True)
    workplace_profile = WorkplaceSupervisorProfileSerializer(source='workplacesupervisor', read_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name', 
            'role', 'phone', 'student_profile', 'academic_profile', 'workplace_profile'
        ]

# --- LOGIN SERIALIZER (JWT) ---

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Customizing the JWT response to include role and username 
    so React can redirect to the correct dashboard immediately.
    """
    def validate(self, attrs):
        data = super().validate(attrs)
        data['username'] = self.user.username
        data['role'] = self.user.role
        data['full_name'] = self.user.get_full_name()
        return data

# --- DOCUMENT SERIALIZER ---

class InternshipDocumentSerializer(serializers.ModelSerializer):
    # We use a StringRelatedField for the student to show the name, not just the ID
    student_name = serializers.ReadOnlyField(source='student.get_full_name')

    class Meta:
        model = InternshipDocument
        fields = [
            'id', 'student', 'student_name', 'document_name', 
            'file', 'status', 'uploaded_at', 'remarks'
        ]
        read_only_fields = ['student', 'status', 'remarks']    



