from django.urls import path
from . import views

app_name = 'chatbot'

urlpatterns = [
    path('chat/', views.chatbot, name='chatbot'),
    path('chat/<int:conversacion_id>/', views.chatbot, name='chatbot_conversacion'),
    path('chat/api/', views.chatbot_api, name='chatbot_api'),
    path('chat/nueva/', views.nueva_conversacion, name='nueva_conversacion'),
    path('chat/eliminar/<int:conversacion_id>/', views.eliminar_conversacion, name='eliminar_conversacion'),
    path('chat/mensajes/<int:conversacion_id>/', views.obtener_mensajes_conversacion, name='obtener_mensajes'),  # ✅ NUEVA RUTA

]
