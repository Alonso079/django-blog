from django.apps import AppConfig


class DashboardConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'dashboard'

    def ready(self):
        from django.db.models.signals import post_migrate
        from .signals import create_autores_managers_group
        post_migrate.connect(create_autores_managers_group, sender=self)
