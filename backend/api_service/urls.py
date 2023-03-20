from django.urls import path
from .views import CharacterSessionView, LoginSessionView, LogoutSessionView

urlpatterns = [
    path('characterSession', CharacterSessionView.as_view()),
    path('loginSession', LoginSessionView.as_view()),
    path('logoutSession', LogoutSessionView.as_view()),
]