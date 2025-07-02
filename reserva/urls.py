from . import views
from django.urls import path

urlpatterns = [
    path('', views.reservar, name='reservar'),
    path('sucesso/', views.reserva_sucesso, name='reserva_sucesso'),
    path('cancelar/<int:reserva_id>/', views.cancelar_reserva, name='cancelar_reserva'),
]
