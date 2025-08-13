from django.urls import path
from . import views

# This defines the URL patterns for the homoglyph_app.
# We give each URL a name so we can refer to it easily elsewhere.
urlpatterns = [
    # The root URL of the app ('/') will be handled by the index view.
    path('', views.index, name='index'),
    
    # The URL for our detection API ('/api/detect/')
    path('api/detect/', views.detection_api, name='api_detect'),
    
    # The URL for our creation API ('/api/generate/')
    path('api/generate/', views.creation_api, name='api_generate'),

    path('api/shorten/', views.shorten_api, name='api_shorten'),

    path('r/<str:short_code>/', views.redirect_view, name='redirect'),
]