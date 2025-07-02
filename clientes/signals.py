from django.db.models.signals import post_save
from django.dispatch import receiver
from clientes.models import Cliente
from usuarios.models import User

@receiver(post_save, sender=User)
def criar_cliente(sender, instance, created, **kwargs):
    if created:
        Cliente.objects.create(user=instance, tipo='avulso')