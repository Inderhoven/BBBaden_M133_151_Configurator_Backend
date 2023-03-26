from django.urls import path
from .views import CharacterView, AuthUser

urlpatterns = [
    path('character', CharacterView.as_view()),
    path('user', AuthUser.as_view())
]