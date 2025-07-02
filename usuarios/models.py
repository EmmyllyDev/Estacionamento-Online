from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    email = models.EmailField(unique=True, blank=False, null=False)
    nome = models.CharField(max_length=150, blank=True, null=False)
    telefone = models.CharField(max_length=15, blank=True, null=False)
    cpf = models.CharField(max_length=14, unique=True, blank=True, null=True)
    mensalista = models.BooleanField(default=False)
    vaga_mensalista = models.ForeignKey(
        'vagas.Vaga',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='usuarios_mensalistas'
    )

    def __str__(self):
            return self.username  
        
        
        
