from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth.models import Group, Permission

@receiver(post_migrate)
def create_groups_and_permissions(sender, **kwargs):
    # Crear grupos
    autor_group, _ = Group.objects.get_or_create(name='Autor')
    moderador_group, _ = Group.objects.get_or_create(name='Moderador')
    verificador_group, _ = Group.objects.get_or_create(name='Verificador')

    # Asignar permisos al grupo Autor
    autor_permissions = [
        'can_view_author',
        'can_edit_author',
        'can_delete_author'
    ]
    for perm in autor_permissions:
        try:
            permission = Permission.objects.get(codename=perm)
            autor_group.permissions.add(permission)
        except Permission.DoesNotExist:
            print(f"El permiso '{perm}' no existe")
