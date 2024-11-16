import uuid
from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib import admin

from dashboard.models import Autor  # Importar el modelo Autor

# Modelo de Categoría (Categoria)
class Categoria(models.Model):
    nombre = models.CharField(max_length=200, blank=False)
    slug = models.SlugField(unique=True, blank=True)  # Hacer que el slug sea opcional
    imagen = models.CharField(max_length=300, blank=True, default='Sin imagen disponible')
    descripcion = models.CharField(max_length=500, blank=True, default='Sin descripción disponible', verbose_name='Descripción')

    class Meta:
        verbose_name_plural = 'Categorías'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nombre)
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.nombre)

# Modelo de Etiqueta (Tag)
class Etiqueta(models.Model):
    nombre = models.CharField(max_length=100, unique=True, blank=False)
    slug = models.SlugField(unique=True, blank=True)
    descripcion = models.CharField(max_length=300, blank=True, default='Sin descripción', verbose_name='Descripción de la Etiqueta')

    class Meta:
        verbose_name_plural = 'Etiquetas'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nombre)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre

# Modelo de Blog (Blog)
class Blog(models.Model):
    ESTADO = (
        ('activo', 'activo'),
        ('pendiente', 'pendiente'),
        ('aprobado', 'aprobado')  # Nuevo estado para indicar aprobación
    )

    titulo = models.CharField(max_length=200, blank=False, default='Título por defecto')
    detalle = models.TextField(max_length=2000, blank=False, default='Sin detalles disponibles')
    imagen = models.ImageField(upload_to='imagenes/media', blank=True, default='default.jpg')
    categoria = models.ForeignKey(Categoria, on_delete=models.DO_NOTHING, null=True)
    etiquetas = models.ManyToManyField(Etiqueta, blank=True)
    estado = models.CharField(max_length=20, choices=ESTADO, default='pendiente')
    autor = models.ForeignKey(Autor, on_delete=models.CASCADE)
    destacado = models.BooleanField(default=False)
    conteo_visitas = models.IntegerField(default=0)
    visible = models.BooleanField(default=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Blogs'

    def save(self, *args, **kwargs):
        # Aprobar automáticamente si el autor es administrador
        if self.autor.usuario.is_staff or self.autor.usuario.is_superuser:
            self.estado = 'aprobado'
        super().save(*args, **kwargs)

    def resumen(self):
        return self.detalle[:30]

    @property
    def url_imagen(self):
        if self.imagen and hasattr(self.imagen, 'url'):
            return self.imagen.url
        return ''

    def __str__(self):
        return f"{self.titulo} | {self.autor.usuario.username} | {self.estado}"

# Modelo de Comentario (Comentario)
class Comentario(models.Model):
    publicacion = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='comentarios')
    nombre = models.CharField(max_length=100, blank=True, default='Anónimo')
    cuerpo = models.TextField(blank=False, default='Sin comentario')
    creado_en = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=[('pendiente', 'pendiente'), ('aprobado', 'aprobado')], default='pendiente')  # Campo de estado para comentarios

    def save(self, *args, **kwargs):
        # Aprobar automáticamente si el autor del blog es administrador
        if self.publicacion.autor.usuario.is_staff or self.publicacion.autor.usuario.is_superuser:
            self.estado = 'aprobado'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.publicacion.titulo} | {self.nombre} | {self.estado}"

# Modelo de Respuesta (Respuesta)
class Respuesta(models.Model):
    comentario = models.ForeignKey(Comentario, on_delete=models.CASCADE, related_name='respuestas')
    nombre = models.CharField(max_length=200, blank=True, default='Anónimo')
    cuerpo = models.TextField(blank=False, default='Sin respuesta')
    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.comentario} | {self.nombre}"

# Modelo de Registro de Correos Electrónicos (RegistroCorreo)
class RegistroCorreo(models.Model):
    correo = models.EmailField(blank=True, default='correo@ejemplo.com')

    class Meta:
        verbose_name_plural = "Correos de Usuarios"

    def __str__(self):
        return self.correo if self.correo else "Correo no proporcionado"

# Modelo de Contacto (Contacto)
class Contacto(models.Model):
    nombre = models.CharField(max_length=100, blank=False, verbose_name='Nombre')
    correo = models.EmailField(blank=False)
    mensaje = models.TextField(blank=False, default='Sin mensaje')
    asunto = models.CharField(max_length=200, blank=False, verbose_name='Asunto')

    def __str__(self):
        return f"{self.nombre} | {self.asunto}"

# Configuración del administrador para modelos
@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'slug', 'imagen', 'descripcion')
    search_fields = ('nombre', 'descripcion')
    prepopulated_fields = {'slug': ('nombre',)}

@admin.register(Etiqueta)
class EtiquetaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'slug', 'descripcion')
    search_fields = ('nombre', 'descripcion')
    prepopulated_fields = {'slug': ('nombre',)}

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'autor', 'estado', 'creado_en', 'destacado')
    search_fields = ('titulo', 'detalle', 'autor__usuario__username')
    list_filter = ('estado', 'destacado', 'creado_en')
    ordering = ('-creado_en',)
    autocomplete_fields = ['autor', 'categoria', 'etiquetas']

@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ('publicacion', 'nombre', 'creado_en', 'estado')
    search_fields = ('publicacion__titulo', 'nombre', 'cuerpo')
    list_filter = ('estado', 'creado_en')

@admin.register(Respuesta)
class RespuestaAdmin(admin.ModelAdmin):
    list_display = ('comentario', 'nombre', 'creado_en')
    search_fields = ('comentario__cuerpo', 'nombre', 'cuerpo')
    list_filter = ('creado_en',)

@admin.register(RegistroCorreo)
class RegistroCorreoAdmin(admin.ModelAdmin):
    list_display = ('correo',)
    search_fields = ('correo',)

@admin.register(Contacto)
class ContactoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'correo', 'asunto')
    search_fields = ('nombre', 'correo', 'asunto', 'mensaje')
