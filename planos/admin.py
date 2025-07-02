from django.contrib import admin

from planos.models import PedidoPlano, Plano

# Register your models here.

@admin.register(Plano)
class PlanoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'valor')
    search_fields = ('nome',)

@admin.register(PedidoPlano)
class PedidoPlanoAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'plano', 'data_vencimento', 'pago', 'data_pedido')
    list_filter = ('pago', 'plano')
    search_fields = ('cliente__user__username',)
    readonly_fields = ('data_pedido',)
    actions = ['marcar_como_pago']

    def marcar_como_pago(self, request, queryset):
        updated = queryset.update(pago=True)
        self.message_user(request, f"{updated} pedido(s) marcado(s) como pago(s).")
    marcar_como_pago.short_description = "Marcar pedidos selecionados como pagos"