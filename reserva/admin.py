from django.contrib import admin
from .models import Reserva 

@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'vaga', 'data_prevista', 'hora_entrada', 'hora_saida', 'email', 'telefone', 'pago')
    search_fields = ('cliente__username', 'vaga__numero', 'email')
    list_filter = ('pago', 'data_prevista')
    ordering = ('-data_prevista',)
    
    def permissao(self, request):
        return False