from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import InternshipDocument,Student,AcademicSupervisor,WorkplaceSupervisor,User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer,RefreshToken
from django.db import transaction



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
        fields=['organization_name']

#user serializer

class UserSerializer(serializers.ModelSerializer):
    # these  will be populated based on user role
    student_profile=StudentProfileSerializer(source='student',read_only=True)
    academic_profile=AcademicProfileSerializer(source="academicsupervisor",read_only=True)
    workplace_profile=WorkPlaceProfileSerializer(source='workplacesupervisor',read_only=True)

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
    


User = get_user_model()


#registrationserializer

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    registration_number = serializers.CharField(required=True)
    course = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name', 'role', 'registration_number', 'course']

    # FIX 1: Move this OUTSIDE of the create method. 
    # It must be aligned with the "def create" line.
    def validate_registration_number(self, value):
        if Student.objects.filter(registration_number=value).exists():
            raise serializers.ValidationError("This registration number is already registered.")
        return value

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("This username is already taken.")
        return value

    # FIX 2: Ensure this is a SEPARATE method
    def create(self, validated_data):
        with transaction.atomic():
            reg_no = validated_data.pop('registration_number', None)
            course = validated_data.pop('course', None)
            
            user = User.objects.create_user(**validated_data)

            if user.role == User.Role.STUDENT:
                Student.objects.create(user=user, registration_number=reg_no, course=course)
            
            return user



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



