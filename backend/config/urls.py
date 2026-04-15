
from django.contrib import admin
from django.urls import path,include
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static
from .views import home
from users.views import InternshipDocumentViewSet  # Look in the users app!
from django.contrib import admin

from drf_spectacular.views import (
    SpectacularAPIView, 
    SpectacularRedocView, 
    SpectacularSwaggerView
)

# Create a router and register our viewset
router = DefaultRouter()
router.register(r'documents', InternshipDocumentViewSet, basename='internship-document')


# Customizing the Admin Interface titles
admin.site.site_header = "Internship Placement System"
admin.site.site_title = "IPS Admin Portal"
admin.site.index_title = "Welcome to the IPS Management Dashboard"

urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),


    path('api/', include(router.urls)), # This "hooks up" the documents endpoints
    #the Schema (the raw data)
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    
    # 2. Swagger UI (The interactive dashboard)
    path('api/docs/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    
    # 3. Redoc (Optional alternative view)
    path('api/docs/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),



]




# This allows the browser to access files in the media folder during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


