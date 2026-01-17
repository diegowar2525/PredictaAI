from django.urls import path
from . import views

app_name = 'gameplay'

urlpatterns = [
<<<<<<< HEAD
    path('chat/', views.chatbot, name='chatbot'),
]
=======
    path("start-game/", game_view, name="start-game")    
]
>>>>>>> a58b910b41f99139328e9c13ccc0764f290c5e69
