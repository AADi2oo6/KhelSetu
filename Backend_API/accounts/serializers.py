# accounts/serializers.py
from rest_framework import serializers
from .models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        # List all the fields from your Profile model that you want to include
        fields = [
            'first_name', 
            'last_name', 
            'phone_number', 
            'date_of_birth',
            'age',
            'address_line_1', 
            'city', 
            'state', 
            'profile_image_url', 
            'height', 
            'weight'
        ]