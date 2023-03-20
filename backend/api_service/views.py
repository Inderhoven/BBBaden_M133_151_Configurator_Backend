from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework.settings import settings

import jwt

# Create your views here.
class CharacterSessionView(APIView):
    def get(self, request):
        session_key = request.COOKIES.get('sessionid')
        if session_key:
            request.session['session_key'] = session_key
            character_settings = request.session.get('characterSettings', [])
            gender = character_settings[0] if character_settings else ''
            hairColor = character_settings[1] if character_settings else ''
            eyeColor = character_settings[2] if character_settings else ''
            name = character_settings[3] if character_settings else ''
            profession = character_settings[4] if character_settings else ''
        else:
            response = {
                "message" : "no Session found"
            }
            return JsonResponse(response)

        response = {
            'sessionid': session_key,
            'gender': gender,
            'hairColor': hairColor,
            'eyeColor': eyeColor,
            'name': name,
            'profession': profession
        }
        return JsonResponse(response)

    def post(self, request):
        session_key = request.COOKIES.get('sessionid')
        if not session_key:
            response = {
                "message": "no Session found"
            }
            return JsonResponse(response)

        gender = request.data.get('gender', '')
        hairColor = request.data.get('hairColor', '')
        eyeColor = request.data.get('eyeColor', '')
        name = request.data.get('name', '')
        profession = request.data.get('profession', '')
        character_settings = [gender, hairColor, eyeColor, name, profession]
        request.session['characterSettings'] = character_settings

        response = {
            'sessionid': session_key,
            'gender': gender,
            'hairColor': hairColor,
            'eyeColor': eyeColor,
            'name': name,
            'profession': profession
        }
        return JsonResponse(response)
    
class LoginSessionView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            request.session.create()
            session_key = request.session.session_key
            response = JsonResponse({'sessionid': session_key})
            response.set_cookie('sessionid', session_key)
            
            return response
        else:
            response = Response()
            response.status_code = 401
            
            return response
        
class LogoutSessionView(APIView):
    def post(self, request):
        request.session.flush()

        response = JsonResponse({'message': 'Logged out successfully.'})
        response.delete_cookie('sessionid')

        return response
    
class LoginJWTView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            jwtData = {
                'username': username,
            }

            token = jwt.encode(jwtData, settings.JWT_SECRET_KEY, algorithm='HS256')

            response = Response({'jwt' : token})
            response.set_cookie('jwt', token)

            return response
        else:
            response = Response()
            response.status_code = 401

            return response
        
class LogoutJWTView(APIView):
    def post(self, request):
        response = JsonResponse({'message': 'Logged out successfully.'})
        response.delete_cookie('jwt')

        return response

class CharacterJWTView(APIView):
    pass