from django.urls import path
from . import views

app_name = 'vagas'

urlpatterns = [
    path('', views.lista_vagas, name='lista_vagas'),
    path('confirmar_vaga', views.confirmar_vaga, name='confirmar_vaga'),
]