from django.urls import path
from . import views

app_name = 'pagamentos'

urlpatterns = [
    path('', views.pagamento, name='pagamento'),
    path('recibo/', views.recibo, name='recibo'),
    path('pagamento-mensalista/', views.pagamento_mensalista, name='pagamento_mensalista'),
    path('pagamento-confirmado/<int:pedido_id>/', views.confirmar_pagamento, name='confirmar_pagamento'),
]