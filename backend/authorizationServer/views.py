from rest_framework.views import APIView
from django.conf import settings
from rest_framework import authentication, exceptions
from django.contrib.auth.models import User

import jwt


# Create your views here.
class CharacterView(APIView):
    def post(self, request):
        pass

    def get(self, request):
        auth_header = authentication.get_authorization_header(request)
        if not auth_header:
            return None
        
        try:
            token = auth_header.decode('utf-8')
            payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=['HS256'])

        except:
            raise exceptions.AuthenticationFailed('Invalid authentication token')
        
        try:
            user = User.objects.get(id=payload['userId'])
        except:
            raise exceptions.AuthenticationFailed('User not found')
        
        pass