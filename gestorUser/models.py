from django.db import models
from django.contrib.auth.models import User

class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rol = models.CharField(max_length=20, choices=[
        ('admin', 'Administrador'),
        ('normal', 'Usuario Normal'),
    ])

    def __str__(self):
        return f"{self.user.username} ({self.rol})"
