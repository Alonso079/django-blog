from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth.models import Group, Permission  # Importa Permission aquí
from django.contrib.contenttypes.models import ContentType
from .models import Autor

@receiver(post_migrate)
def create_autores_managers_group(sender, **kwargs):
    if sender.name.endswith('dashboard'):  # Verifica que el remitente sea tu app
        group, created = Group.objects.get_or_create(name='Autores Managers')
        if created:
            try:
                content_type = ContentType.objects.get_for_model(Autor)
                permissions = Permission.objects.filter(content_type=content_type)
                group.permissions.set(permissions)
                print(f"Grupo 'Autores Managers' creado con {permissions.count()} permisos.")
            except Exception as e:
                print(f"Error asignando permisos: {e}")
