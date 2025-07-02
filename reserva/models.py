from django.db import models

class Reserva(models.Model):
    cliente = models.ForeignKey(
        'usuarios.User',
        on_delete=models.CASCADE,
        related_name='reservas'
    )
    vaga = models.ForeignKey(
        'vagas.Vaga',
        on_delete=models.CASCADE,
        related_name='reservas'
    )
    data_prevista = models.DateField()
    hora_entrada = models.TimeField()
    hora_saida = models.TimeField()
    email = models.EmailField()
    telefone = models.CharField(max_length=15)
    pago = models.BooleanField(default=False)

    def __str__(self):
        return f"Reserva {self.id} - {self.cliente.username} - Vaga {self.vaga.numero} - Data{self.data_prevista} - Hora Entrada{self.hora_entrada} - Hora Saida {self.hora_saida} - {'Pago' if self.pago else 'Pendente'}"