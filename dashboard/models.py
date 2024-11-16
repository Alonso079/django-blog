from django.db import models
from django.contrib.auth.models import User


from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import Group, Permission
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.models import ContentType

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
        permissions = [
            ("can_view_author", "Puede ver el autor"),
            ("can_edit_author", "Puede editar el autor"),
            ("can_delete_author", "Puede eliminar el autor"),
        ]

    def __str__(self):
        return self.usuario.username

# Configuración del administrador para Autor
from django.contrib import admin

@admin.register(Autor)
class AutorAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'nombre', 'apellido', 'cargo', 'estado_autor')
    search_fields = ('usuario__username', 'nombre', 'apellido', 'correo')
    list_filter = ('cargo', 'estado_autor')
    ordering = ('usuario',)

    def get_queryset(self, request):
        # Filtrar la vista para que los administradores solo puedan ver autores que tienen permisos específicos
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        if request.user.groups.filter(name='Autores Managers').exists():
            return qs
        return qs.filter(usuario=request.user)

    def has_view_permission(self, request, obj=None):
        # Permitir la visualización según los permisos del usuario
        if request.user.is_superuser:
            return True
        if request.user.groups.filter(name='Autores Managers').exists() or request.user.has_perm('app.can_view_author'):
            return True
        return False

    def has_change_permission(self, request, obj=None):
        # Permitir la edición según los permisos del usuario
        if request.user.is_superuser:
            return True
        if request.user.groups.filter(name='Autores Managers').exists() or request.user.has_perm('app.can_edit_author'):
            return True
        return False

    def has_delete_permission(self, request, obj=None):
        # Permitir la eliminación según los permisos del usuario
        if request.user.is_superuser:
            return True
        if request.user.groups.filter(name='Autores Managers').exists() or request.user.has_perm('app.can_delete_author'):
            return True
        return False

    def has_module_permission(self, request):
        # Controlar el acceso a la sección de Autores en el menú del administrador
        if request.user.is_superuser:
            return True
        if request.user.groups.filter(name='Autores Managers').exists() or request.user.has_perm('app.can_view_author'):
            return True
        return False

    def get_readonly_fields(self, request, obj=None):
        # Hacer que ciertos campos sean de solo lectura si el usuario no tiene permisos de edición
        if not request.user.is_superuser and not request.user.groups.filter(name='Autores Managers').exists() and not request.user.has_perm('app.can_edit_author'):
            return [f.name for f in self.model._meta.fields]
        return super().get_readonly_fields(request, obj)

    def get_fields(self, request, obj=None):
        # Restringir los campos visibles según los permisos del usuario
        fields = super().get_fields(request, obj)
        if not request.user.is_superuser and not request.user.groups.filter(name='Autores Managers').exists() and not request.user.has_perm('app.can_edit_author'):
            return [f for f in fields if f not in ['correo', 'imagen_autor']]
        return fields
