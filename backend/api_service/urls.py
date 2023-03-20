from django.urls import path
from .views import CharacterSessionView, LoginSessionView, LogoutSessionView, LoginJWTView, LogoutJWTView, CharacterJWTView

urlpatterns = [
    path('characterSession', CharacterSessionView.as_view()),
    path('characterJWT', CharacterJWTView.as_view()),
    path('loginSession', LoginSessionView.as_view()),
    path('loginJWT', LoginJWTView.as_view()),
    path('logoutSession', LogoutSessionView.as_view()),
    path('logoutJWT', LogoutJWTView.as_view())
]