# backend/urls.py
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from accounts.views import  RegisterFaceView, ProfileViewSet, VerifyFaceView # <-- Import VerifyFaceView
from chatbot.views import ChatbotView
# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'profile', ProfileViewSet, basename='profile')

urlpatterns = [
    # path('', home_page, name='home'),
    path('admin/', admin.site.urls),
    
    # Add the router's URLs to our urlpatterns.
    # This will create an endpoint at /api/profile/
    path('api/', include(router.urls)), 
    path('api/chatbot/', ChatbotView.as_view(), name='chatbot'),
    
    # Existing auth and face registration URLs
    path('api/auth/', include('djoser.urls')),
    path('api/auth/', include('djoser.urls.authtoken')),
    path('api/face/register/', RegisterFaceView.as_view(), name='register-face'),
    path('api/face/verify/', VerifyFaceView.as_view(), name='verify-face'),

]