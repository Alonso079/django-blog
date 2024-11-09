import uuid
from django.db import models
from django.utils.text import slugify
from dashboard.models import Autor

# Modelo de Categoría (Categoria)
class Categoria(models.Model):
    nombre = models.CharField(max_length=200, blank=False)
    slug = models.SlugField(unique=True, blank=True)  # Hacer que el slug sea opcional
    imagen = models.CharField(max_length=300, blank=True)
    descripcion = models.CharField(max_length=500, blank=True, verbose_name='Descripción')

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
    descripcion = models.CharField(max_length=300, blank=True, verbose_name='Descripción de la Etiqueta')

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
        ('pendiente', 'pendiente')
    )

    titulo = models.CharField(max_length=200, blank=False)
    detalle = models.TextField(max_length=2000, blank=False)
    imagen = models.ImageField(upload_to='imagenes/media', blank=True)
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
    nombre = models.CharField(max_length=100, blank=True)
    cuerpo = models.TextField(blank=False)
    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.publicacion.titulo} | {self.nombre}"

# Modelo de Respuesta (Respuesta)
class Respuesta(models.Model):
    comentario = models.ForeignKey(Comentario, on_delete=models.CASCADE, related_name='respuestas')
    nombre = models.CharField(max_length=200, blank=True)
    cuerpo = models.TextField(blank=False)
    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.comentario} | {self.nombre}"

# Modelo de Registro de Correos Electrónicos (RegistroCorreo)
class RegistroCorreo(models.Model):
    correo = models.EmailField(blank=True)

    class Meta:
        verbose_name_plural = "Correos de Usuarios"

    def __str__(self):
        return self.correo if self.correo else "Correo no proporcionado"

# Modelo de Contacto (Contacto)
class Contacto(models.Model):
    nombre = models.CharField(max_length=100, blank=False, verbose_name='Nombre')
    correo = models.EmailField(blank=False)
    mensaje = models.TextField(blank=False)
    asunto = models.CharField(max_length=200, blank=False, verbose_name='Asunto')

    def __str__(self):
        return f"{self.nombre} | {self.asunto}"
