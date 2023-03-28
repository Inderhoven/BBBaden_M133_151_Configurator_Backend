from rest_framework.views import APIView
from django.conf import settings
from rest_framework import authentication, exceptions, serializers
from django.contrib.auth.models import User
from rest_framework.response import Response
from django.http import JsonResponse
from .models import CharacterSettings
from datetime import datetime, timedelta

import jwt, pytz


# Create your views here.
class CharacterSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CharacterSettings
        fields = '__all__'

class CharacterView(APIView):

    def _authenticate_user(self, request):
        auth_header = authentication.get_authorization_header(request)
        if not auth_header:
            raise exceptions.AuthenticationFailed('Authorization header is missing')
        
        try:
            token = auth_header.decode('utf-8')
            payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=['HS256'])
            user = User.objects.get(id=payload['userId'])
        except jwt.exceptions.DecodeError:
            raise exceptions.AuthenticationFailed('Invalid authentication token')
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('User not found')
        
        return user

    def post(self, request):
        user = self._authenticate_user(request)

        if user is not None:
            gender = request.data.get('gender', '')
            hairColor = request.data.get('hairColor', '')
            eyeColor = request.data.get('eyeColor', '')
            name = request.data.get('name', '')
            profession = request.data.get('profession', '')

            character_settings, created = CharacterSettings.objects.get_or_create(user=user)

            if not created:
                character_settings.gender = gender
                character_settings.hairColor = hairColor
                character_settings.eyeColor = eyeColor
                character_settings.name = name
                character_settings.profession = profession
                character_settings.save()
            
            else:
                character_settings.user = user
                character_settings.gender = gender
                character_settings.hairColor = hairColor
                character_settings.eyeColor = eyeColor
                character_settings.name = name
                character_settings.profession = profession
                character_settings.save()
                
            serializer = CharacterSettingsSerializer(character_settings)

            return Response(serializer.data, status=201)


        return Response({'message': 'Not authenticated!'}, status=401)

    def get(self, request):
        user = self._authenticate_user(request)

        if user is not None:

            try:
                character_settings = CharacterSettings.objects.get(user=user)
                serializer = CharacterSettingsSerializer(character_settings)
                return Response(serializer.data)

            except:
                return Response({'message': 'No User data found'})             
        
        return Response({'message': 'Not authenticated!'}, status=401)
    
class AuthUser(APIView):

    def _authenticate_user(self, request):
        auth_header = authentication.get_authorization_header(request)
        if not auth_header:
            raise exceptions.AuthenticationFailed('Authorization header is missing')
        
        try:
            token = auth_header.decode('utf-8')
            payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=['HS256'])
            user = User.objects.get(id=payload['userId'])

            #check if the token has expired
            if 'exp' in payload:
                expiration_time = datetime.utcfromtimestamp(payload['exp']).replace(tzinfo=pytz.UTC)
                print("time", expiration_time)
                print("time2", datetime.utcnow().replace(tzinfo=pytz.UTC))
                if datetime.utcnow().replace(tzinfo=pytz.UTC) > expiration_time:
                    raise exceptions.AuthenticationFailed('Token has expired')
        except jwt.exceptions.DecodeError:
            raise exceptions.AuthenticationFailed('Invalid authentication token')
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('User not found')
        
        return user
    
    def post(self, request):
        try:
            user = self._authenticate_user(request)
        except:
            return Response({'message': 'Not Authorized'}, status=401)
            

        if user is not None:
            return Response({'message' : 'success'}, status=200)
        
        else:
            return Response({'message': 'Not Authorized'},status=401)

class RefreshToken(APIView):

    def post(self, request):
        refresh_token = request.COOKIES.get('refresh_token')
        print("Headers", request.COOKIES)
        print("Refresh Token: ", refresh_token)
        if refresh_token is None:
            raise exceptions.AuthenticationFailed('Refresh token is missing')
        
        try:
            payload = jwt.decode(refresh_token, settings.JWT_REFRESH_SECRET_KEY, algorithms=['HS256'])
            user = User.objects.get(id=payload['userId'])
        except jwt.exceptions.DecodeError:
            raise exceptions.AuthenticationFailed('Invalid refresh token')
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('User not found')
        
        if not user.is_active:
            raise exceptions.AuthenticationFailed('User is inactive')
        
        access_token_expiry = datetime.utcnow().replace(tzinfo=pytz.UTC) + timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRATION_MINUTES)
        access_token_payload = {'userId' : user.id, 'exp': int(access_token_expiry.timestamp()), 'type': 'access'}
        access_token = jwt.encode(access_token_payload, settings.JWT_SECRET_KEY, algorithm='HS256')

        response = Response({'userId' : user.id, 'type': 'access'})
        response.set_cookie('jwt', access_token)

        return response