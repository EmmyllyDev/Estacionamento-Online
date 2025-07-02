from django.db import models
from django.utils import timezone
from usuarios.models import User

class Vaga(models.Model):
    numero = models.IntegerField(unique=True)
    ocupada = models.BooleanField(default=False)
    tipo_cliente = models.CharField(
        max_length=10,
        choices=[('avulso', 'Avulso'), ('mensalista', 'Mensalista')],
        default='avulso'
    )
    cliente_mensalista = models.ForeignKey(
        'clientes.Mensalista',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='vagas',
        help_text='Cliente associado se a vaga for de um mensalista.'
    )

    def __str__(self):
        return f"Vaga {self.numero} - {'Ocupada' if self.ocupada else 'Livre'}"
    
    
class EntradaVeiculo(models.Model):
    cliente = models.ForeignKey(User, on_delete=models.CASCADE, related_name='entradas')
    vaga = models.ForeignKey(Vaga, on_delete=models.SET_NULL, null=True)
    data_entrada = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Entrada de {self.cliente.username} em {self.data_entrada}"

class SaidaVeiculo(models.Model):
    cliente = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saidas')
    vaga = models.ForeignKey(Vaga, on_delete=models.SET_NULL, null=True)
    data_saida = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Saída de {self.cliente.username} em {self.data_saida}"