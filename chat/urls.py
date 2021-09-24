# chat/urls.py
from django.urls import path

from . import views
app_name='chat'
urlpatterns = [
    path('', views.index, name='index'),
    path('vero/', views.veroJSON, name='veroJSON'),
    path('<str:room_name>/', views.room, name='room'),
]