
from django.db import models
from django.contrib.auth.models import User

from datetime import date # <-- Import this

class Profile(models.Model):
    # ... (all your existing fields are here) ...
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    face_encoding = models.TextField(blank=True, null=True)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    date_of_birth = models.DateField(blank=True, null=True)
    age = models.PositiveIntegerField(blank=True, null=True)
    address_line_1 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    profile_image_url = models.URLField(max_length=500, blank=True)
    height = models.FloatField(blank=True, null=True, help_text="Height in centimeters")
    weight = models.FloatField(blank=True, null=True, help_text="Weight in kilograms")
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return f'{self.user.username} Profile'

    # --- Add this method ---
    def save(self, *args, **kwargs):
        if self.date_of_birth:
            today = date.today()
            # Calculate age based on year, month, and day
            self.age = today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
        else:
            self.age = None
        
        # Call the original save method to save the instance
        super().save(*args, **kwargs)
