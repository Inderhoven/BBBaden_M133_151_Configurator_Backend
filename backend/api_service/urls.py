from django.urls import path
from .views import CharacterSessionView, LoginSessionView, LogoutSessionView, UserAuth

urlpatterns = [
    path('characterSession', CharacterSessionView.as_view()),
    path('loginSession', LoginSessionView.as_view()),
    path('logoutSession', LogoutSessionView.as_view()),
    path('user', UserAuth.as_view())
]