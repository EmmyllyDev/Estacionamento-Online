from django.db import models
from planos.models import Plano
from usuarios.models import User

class Cliente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=10, choices=[('avulso', 'Avulso'), ('mensalista', 'Mensalista')], default='avulso')

    def __str__(self):
        return self.user.username

class Mensalista(models.Model):
    cliente = models.OneToOneField(Cliente, on_delete=models.CASCADE)
    plano = models.ForeignKey(Plano, on_delete=models.SET_NULL, null=True)
    vaga = models.OneToOneField('vagas.Vaga', on_delete=models.SET_NULL, null=True, blank=True)
    contrato_ativo = models.BooleanField(default=False)
    data_inicio = models.DateField(null=True, blank=True)
    data_vencimento = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.cliente.user.username} - {self.plano.nome if self.plano else 'Sem Plano'}"
    
