from rest_framework import serializers
from .models import InternshipDocument

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = InternshipDocument
        fields = ['id', 'document_name', 'file', 'status', 'uploaded_at', 'remarks']
        read_only_fields = ['status', 'uploaded_at'] # Students can't approve their own docs!