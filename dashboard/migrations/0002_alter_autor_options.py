# Generated by Django 5.1.1 on 2024-11-16 21:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='autor',
            options={'permissions': [('can_view_author', 'Puede ver el autor'), ('can_edit_author', 'Puede editar el autor'), ('can_delete_author', 'Puede eliminar el autor')], 'verbose_name': 'Autor', 'verbose_name_plural': 'Autores'},
        ),
    ]
