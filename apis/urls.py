from django.urls import path
from . import views

urlpatterns = [
    # Basic page routes
    path('', views.home, name='home'),
    path('submit/', views.submit_form, name='submit_form'),
    path('display/', views.display_data, name='display_data'),
    
    # API route
    path('api/data/', views.get_api_data, name='get_api_data'),
]

# Register error handlers
handler404 = views.handler404