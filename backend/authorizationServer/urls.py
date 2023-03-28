from django.urls import path
from .views import CharacterView, AuthUser, RefreshToken

urlpatterns = [
    path('character', CharacterView.as_view()),
    path('user', AuthUser.as_view()),
    path('refresh', RefreshToken.as_view())
]