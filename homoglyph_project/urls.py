from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # The Django admin site is still available, but not our focus.
    path('admin/', admin.site.urls),
    
    # This is the crucial line:
    # It tells Django to send any request that isn't for '/admin/'
    # to the 'homoglyph_app.urls' file for further processing.
    path('', include('homoglyph_app.urls')),
]