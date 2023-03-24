from rest_framework.views import APIView
from django.conf import settings
from rest_framework import authentication, exceptions, serializers
from django.contrib.auth.models import User
from rest_framework.response import Response
from django.http import JsonResponse
from .models import CharacterSettings

import jwt


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
            pass


        return Response({'message': 'Not authenticated!'}, status=401)

    def get(self, request):
        user = self._authenticate_user(request)

        if user is not None:
            character_settings = CharacterSettings.objects.get(user=user)
            serializer = CharacterSettingsSerializer(character_settings)
            return Response(serializer.data)
        
        return Response({'message': 'Not authenticated!'}, status=401)
        