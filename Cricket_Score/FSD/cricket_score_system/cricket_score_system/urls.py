# cricket_score_system/urls.py

from django.contrib import admin
from django.urls import path, include # <--- Ensure 'include' is imported here
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    # This line is CRUCIAL: it includes all URLs defined in your 'cricket' app's urls.py
    # It must be the only line that includes 'cricket.urls' to avoid recursion.
    path('', include('cricket.urls')),
]

# Only serve static and media files this way during development (DEBUG=True)
# This part should be correct if it was working before.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
