from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework.settings import settings
from django.contrib.auth.models import User
from .serializers import UserSerializer

import jwt

# Create your views here.

class LoginView(APIView):
    def post(self, request):

        user = authenticate(username=request.data.get('username'), password=request.data.get('password'))

        if user is not None:

            authUser = UserSerializer(user)
            jwtData = {
                'userId': authUser.data['id'],
            }

            token = jwt.encode(jwtData, settings.JWT_SECRET_KEY, algorithm='HS256')

            response = Response({'userId' : authUser.data['id']})
            response.set_cookie('jwt', token)

            return response
        else:
            response = Response()
            response.status_code = 401

            return response
        
class LogoutView(APIView):
    def post(self, request):
        response = JsonResponse({'message': 'Logged out successfully.'})
        response.delete_cookie('jwt')

        return response