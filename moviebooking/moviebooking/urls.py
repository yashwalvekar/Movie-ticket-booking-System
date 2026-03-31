"""
URL configuration for moviebooking project.
All routes are delegated to the tickets app.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static  # Needed to serve uploaded images in dev

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('tickets.urls')),  # Include all tickets app URLs
]

# Serve uploaded media files (posters) during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
