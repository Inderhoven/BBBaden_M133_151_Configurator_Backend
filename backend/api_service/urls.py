from django.urls import path
from .views import CharacterSessionView, LoginSessionView

urlpatterns = [
    path('characterSession', CharacterSessionView.as_view()),
    path('loginSession', LoginSessionView.as_view())
]