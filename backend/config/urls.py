from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import home # Ensure this view exists in your config/views.py

from drf_spectacular.views import (
    SpectacularAPIView, 
    SpectacularRedocView, 
    SpectacularSwaggerView
)

# Customizing the Admin Interface titles
admin.site.site_header = "Internship Placement System"
admin.site.site_title = "IPS Admin Portal"
admin.site.index_title = "Welcome to the IPS Management Dashboard"

urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    
    # This ONE line handles tokens, users, and documents 
    # because we put the router inside users.urls
    path('api/', include('users.urls')),

    # API Documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/docs/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

# Media file access for development (PDF uploads)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)