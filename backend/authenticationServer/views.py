from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework.settings import settings
from django.contrib.auth.models import User
from .serializers import UserSerializer
from datetime import datetime, timedelta

import jwt, pytz

# Create your views here.

class LoginView(APIView):
    def post(self, request):

        user = authenticate(username=request.data.get('username'), password=request.data.get('password'))

        if user is not None:

            authUser = UserSerializer(user)

            #Create access token
            access_token_expiry = datetime.utcnow().replace(tzinfo=pytz.UTC) + timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRATION_MINUTES)
            access_token_payload = {
                'exp': access_token_expiry,
                'userId' : authUser.data['id'],
                'type': 'access'
            }
            access_token = jwt.encode(access_token_payload, settings.JWT_SECRET_KEY, algorithm='HS256')

            #Create refresh token
            refresh_token_expiry = datetime.utcnow().replace(tzinfo=pytz.UTC) + timedelta(days=settings.JWT_REFRESH_TOKEN_EXPIRY_DAYS)
            print(refresh_token_expiry)
            refresh_token_payload = {
                'exp' : refresh_token_expiry,
                'userId' : authUser.data['id'],
                'type' : 'refresh'
            }
            refresh_token = jwt.encode(refresh_token_payload, settings.JWT_REFRESH_SECRET_KEY, algorithm='HS256')

            response = Response({'jwt' : access_token_payload, 'refresh': refresh_token_payload})
            response.set_cookie('jwt', access_token)
            response.set_cookie('refresh_token', refresh_token)

            return response
        else:
            response = Response()
            response.status_code = 401

            return response

        # if user is not None:

        #     authUser = UserSerializer(user)
        #     jwtData = {
        #         'userId': authUser.data['id'],
        #         'type': 'access'
        #     }

        #     token = jwt.encode(jwtData, settings.JWT_SECRET_KEY, algorithm='HS256')

        #     response = Response({'userId' : authUser.data['id'], 'type': 'access'})
        #     response.set_cookie('jwt', token)

        #     return response
        # else:
        #     response = Response()
        #     response.status_code = 401

        #     return response
        
class LogoutView(APIView):
    def post(self, request):
        response = JsonResponse({'message': 'Logged out successfully.'})
        response.delete_cookie('jwt')
        response.delete_cookie('refresh_token')

        return response