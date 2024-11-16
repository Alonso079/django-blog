# Generated by Django 5.1.1 on 2024-11-14 02:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='es_aprobado',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='comentario',
            name='es_aprobado',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='blog',
            name='detalle',
            field=models.TextField(default='Sin detalles disponibles', max_length=2000),
        ),
        migrations.AlterField(
            model_name='blog',
            name='imagen',
            field=models.ImageField(blank=True, default='default.jpg', upload_to='imagenes/media'),
        ),
        migrations.AlterField(
            model_name='blog',
            name='titulo',
            field=models.CharField(default='Título por defecto', max_length=200),
        ),
        migrations.AlterField(
            model_name='categoria',
            name='descripcion',
            field=models.CharField(blank=True, default='Sin descripción disponible', max_length=500, verbose_name='Descripción'),
        ),
        migrations.AlterField(
            model_name='categoria',
            name='imagen',
            field=models.CharField(blank=True, default='Sin imagen disponible', max_length=300),
        ),
        migrations.AlterField(
            model_name='categoria',
            name='nombre',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='categoria',
            name='slug',
            field=models.SlugField(blank=True, unique=True),
        ),
        migrations.AlterField(
            model_name='comentario',
            name='cuerpo',
            field=models.TextField(default='Sin comentario'),
        ),
        migrations.AlterField(
            model_name='comentario',
            name='nombre',
            field=models.CharField(blank=True, default='Anónimo', max_length=100),
        ),
        migrations.AlterField(
            model_name='contacto',
            name='asunto',
            field=models.CharField(max_length=200, verbose_name='Asunto'),
        ),
        migrations.AlterField(
            model_name='contacto',
            name='correo',
            field=models.EmailField(max_length=254),
        ),
        migrations.AlterField(
            model_name='contacto',
            name='mensaje',
            field=models.TextField(default='Sin mensaje'),
        ),
        migrations.AlterField(
            model_name='contacto',
            name='nombre',
            field=models.CharField(max_length=100, verbose_name='Nombre'),
        ),
        migrations.AlterField(
            model_name='etiqueta',
            name='descripcion',
            field=models.CharField(blank=True, default='Sin descripción', max_length=300, verbose_name='Descripción de la Etiqueta'),
        ),
        migrations.AlterField(
            model_name='etiqueta',
            name='nombre',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='etiqueta',
            name='slug',
            field=models.SlugField(blank=True, unique=True),
        ),
        migrations.AlterField(
            model_name='registrocorreo',
            name='correo',
            field=models.EmailField(blank=True, default='correo@ejemplo.com', max_length=254),
        ),
        migrations.AlterField(
            model_name='respuesta',
            name='cuerpo',
            field=models.TextField(default='Sin respuesta'),
        ),
        migrations.AlterField(
            model_name='respuesta',
            name='nombre',
            field=models.CharField(blank=True, default='Anónimo', max_length=200),
        ),
    ]
