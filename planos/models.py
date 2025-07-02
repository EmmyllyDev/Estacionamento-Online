from django.db import models


# Create your models here.

class Plano(models.Model):
    nome = models.CharField(max_length=50)  
    descricao = models.TextField(blank=True)
    valor = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return self.nome
    
class PedidoPlano(models.Model):
    cliente = models.ForeignKey('clientes.Cliente', on_delete=models.CASCADE)
    plano = models.ForeignKey(Plano, on_delete=models.CASCADE)
    data_vencimento = models.DateField()
    pago = models.BooleanField(default=False)
    data_pedido = models.DateTimeField(auto_now_add=True)

    mensalista = models.OneToOneField('clientes.Mensalista', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Pedido de {self.cliente.user.username} para {self.plano.nome}"