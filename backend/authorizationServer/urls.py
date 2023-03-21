from django.urls import path
from .views import CharacterView

urlpatterns = [
    path('character', CharacterView.as_view())
]