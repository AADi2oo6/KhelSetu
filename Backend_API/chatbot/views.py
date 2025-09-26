
import os
import google.generativeai as genai
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

# Configure the Gemini API client from the environment variable
try:
    genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
except AttributeError:
    print("GEMINI_API_KEY not found in environment variables.")

class ChatbotView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user_message = request.data.get('message')
        if not user_message:
            return Response({'error': 'No message provided.'}, status=400)

        try:
            # Initialize the generative model
            model = genai.GenerativeModel('gemini-2.0-flash')
            system_prompt = (
                "You are a helpful assistant for a mobile app. "
                "Keep your answers concise and short. "
                "Limit your response to a maximum of 3-4 sentences."
            )
            full_prompt = f"{system_prompt}\n\nUser Question: {user_message}"
            # Send the message and get the response
            response = model.generate_content(full_prompt)
            
            # Prepare the data to send back to the client
            response_data = {
                'user_message': user_message,
                'bot_response': response.text
            }
            
            return Response(response_data, status=200)

        except Exception as e:
            # Handle potential API errors
            return Response({'error': f'An error occurred with the AI service: {str(e)}'}, status=500)