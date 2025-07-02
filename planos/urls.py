from django.urls import path
from . import views

app_name = 'planos'
urlpatterns = [
    path('solicitar-plano/', views.solicitar_plano, name='solicitar_plano'),
]