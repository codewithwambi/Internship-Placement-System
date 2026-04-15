from rest_framework import viewsets
from .models import InternshipDocument
from .serializers import DocumentSerializer

class InternshipDocumentViewSet(viewsets.ModelViewSet):
    queryset = InternshipDocument.objects.all()
    serializer_class = DocumentSerializer      

    
    def perform_create(self, serializer):
        # Professional logic: Automatically assign the logged-in student
        # and set a 'checked' timestamp or log the event.
        serializer.save(student=self.request.user)
        print(f"Document Checker: New file uploaded by {self.request.user}")