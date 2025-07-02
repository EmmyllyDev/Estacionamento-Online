from django.contrib import admin

from clientes.models import Cliente, Mensalista

# Register your models here.
@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('user', 'tipo')
    search_fields = ('user__username',)
    list_filter = ('tipo',)

@admin.register(Mensalista)
class MensalistaAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'plano', 'vaga', 'contrato_ativo', 'data_inicio', 'data_vencimento')
    list_filter = ('contrato_ativo', 'plano')
    search_fields = ('cliente__user__username',)
