from django.db import models
from django.contrib.auth.models import User


# Modelo de Autor
class Autor(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Usuario')
    correo = models.EmailField(unique=True, blank=True, null=True, verbose_name='Correo Electrónico')
    nombre = models.CharField(max_length=100, null=True, blank=True, verbose_name='Nombre')
    apellido = models.CharField(max_length=100, null=True, blank=True, verbose_name='Apellido')
    cargo = models.CharField(max_length=50, null=True, blank=True, verbose_name='Cargo')
    imagen_autor = models.ImageField(upload_to='autores/', verbose_name='Imagen de Perfil del Autor', blank=True, null=True)
    estado_autor = models.CharField(max_length=100, null=True, blank=True, verbose_name='Estado del Autor')

    class Meta:
        verbose_name = 'Autor'
        verbose_name_plural = 'Autores'

    def __str__(self):
        return self.usuario.username
