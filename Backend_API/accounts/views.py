import face_recognition
import numpy as np
# accounts/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Profile, User
import json
# accounts/views.py
# ... (keep all your other existing imports)
from rest_framework.authtoken.models import Token

class VerifyFaceView(APIView):
    # This endpoint does not require authentication
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, *args, **kwargs):
        image_file = request.data.get('image')
        if not image_file:
            return Response({'error': 'No image provided.'}, status=400)

        try:
            # 1. Load the login image and get its encoding
            unknown_image = face_recognition.load_image_file(image_file)
            unknown_encodings = face_recognition.face_encodings(unknown_image)

            if not unknown_encodings:
                return Response({'error': 'No face found in the image.'}, status=400)
            
            unknown_encoding = unknown_encodings[0]

            # 2. Get all profiles with registered face encodings
            profiles_with_faces = Profile.objects.exclude(face_encoding__isnull=True).exclude(face_encoding__exact='')
            
            known_encodings = []
            user_ids = []
            
            for profile in profiles_with_faces:
                # Convert the JSON string from the DB back to a numpy array
                encoding = np.array(json.loads(profile.face_encoding))
                known_encodings.append(encoding)
                user_ids.append(profile.user.id)

            if not known_encodings:
                return Response({'error': 'No faces registered in the system.'}, status=400)

            # 3. Compare the login face with all registered faces
            matches = face_recognition.compare_faces(known_encodings, unknown_encoding)
            
            # 4. Find the first match and log the user in
            for i, match in enumerate(matches):
                if match:
                    user_id = user_ids[i]
                    user = User.objects.get(id=user_id)
                    
                    # Get or create an auth token for the user
                    token, created = Token.objects.get_or_create(user=user)
                    
                    return Response({'auth_token': token.key, 'username': user.username}, status=200)

            # 5. If no match is found after checking all faces
            return Response({'error': 'Verification failed. Face not recognized.'}, status=401)

        except Exception as e:
            return Response({'error': f'An error occurred: {str(e)}'}, status=500)
        
class RegisterFaceView(APIView):
    # Only authenticated users can register their face.
    permission_classes = [IsAuthenticated]
    # Parsers to handle file uploads.
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, *args, **kwargs):
        # 1. Get the image file from the request.
        image_file = request.data.get('image')
        if not image_file:
            return Response({'error': 'No image provided.'}, status=400)

        try:
            # 2. Load the image and find face encodings.
            image = face_recognition.load_image_file(image_file)
            encodings = face_recognition.face_encodings(image)

            # 3. Check if exactly one face was found.
            if len(encodings) == 1:
                # Get the single encoding.
                encoding = encodings[0]

                # 4. Convert the encoding (numpy array) to a JSON string to store in the database.
                encoding_json = json.dumps(encoding.tolist())
                
                # 5. Get or create the user's profile and save the encoding.
                profile, created = Profile.objects.get_or_create(user=request.user)
                profile.face_encoding = encoding_json
                profile.save()

                return Response({'status': 'Face registered successfully.'}, status=200)
            elif len(encodings) > 1:
                return Response({'error': 'More than one face was found in the image.'}, status=400)
            else:
                return Response({'error': 'No face was found in the image.'}, status=400)

        except Exception as e:
            return Response({'error': f'An error occurred: {str(e)}'}, status=500)

from rest_framework import viewsets, permissions
from .models import Profile
from .serializers import ProfileSerializer
# ... (keep all your other existing imports and views)

class ProfileViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to view or edit their profile.
    """
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # This view should only return the profile for the currently authenticated user.
        return Profile.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # When a new profile is created, associate it with the current user.
        serializer.save(user=self.request.user)