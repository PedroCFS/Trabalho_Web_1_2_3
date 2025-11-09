from django.urls import path
from . import views

app_name = 'app_bar'

urlpatterns = [
    path('', views.index, name='index'),
    path('jogos/', views.jogos, name='jogos'),
    path('cardapio/', views.cardapio, name='cardapio'),
]