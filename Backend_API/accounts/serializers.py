# accounts/serializers.py
from rest_framework import serializers
from .models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    # Make 'user' and 'age' read-only fields that are not user-editable
    user = serializers.ReadOnlyField(source='user.username')
    age = serializers.ReadOnlyField()

    class Meta:
        model = Profile
        fields = [
            'id',             # <-- Add this to show the profile's ID
            'user',           # <-- Add this to show the user's name
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
        # read_only_fields = ['user', 'age']