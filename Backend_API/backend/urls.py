# backend/urls.py
from django.contrib import admin
from django.urls import path, include
# You no longer need the router for the profile
from accounts.views import RegisterFaceView, VerifyFaceView, ProfileView # <-- Change ProfileViewSet to ProfileView
from chatbot.views import ChatbotView

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Add the new, simpler path for the profile
    path('api/profile/', ProfileView.as_view(), name='profile'),
    
    path('api/chatbot/', ChatbotView.as_view(), name='chatbot'),
    
    # Existing auth and face registration URLs
    path('api/auth/', include('djoser.urls')),
    path('api/auth/', include('djoser.urls.authtoken')),
    path('api/face/register/', RegisterFaceView.as_view(), name='register-face'),
    path('api/face/verify/', VerifyFaceView.as_view(), name='verify-face'),
]