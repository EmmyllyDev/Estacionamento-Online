from django.contrib import admin
from .models import EntradaVeiculo, SaidaVeiculo, Vaga

@admin.register(Vaga)
class VagaAdmin(admin.ModelAdmin):
    list_display = ('numero', 'ocupada', 'tipo_cliente', 'ultima_entrada', 'ultima_saida')

    def ultima_entrada(self, obj):
        entrada = EntradaVeiculo.objects.filter(vaga=obj).order_by('-data_entrada').first()
        return entrada.data_entrada if entrada else '-'
    ultima_entrada.short_description = 'Última Entrada'

    def ultima_saida(self, obj):
        saida = SaidaVeiculo.objects.filter(vaga=obj).order_by('-data_saida').first()
        return saida.data_saida if saida else '-'
    ultima_saida.short_description = 'Última Saída'