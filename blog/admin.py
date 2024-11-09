from django.contrib import admin
from .models import Autor, Categoria, Blog, Etiqueta, RegistroCorreo, Contacto, Comentario, Respuesta

# Configuración personalizada para el modelo de Autor
class AutorAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'correo', 'nombre', 'apellido', 'cargo')
    search_fields = ('usuario__username', 'nombre', 'apellido')

# Configuración personalizada para el modelo de Categoría
class CategoriaAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('nombre',)}

# Configuración personalizada para el modelo de Blog
class BlogAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'autor', 'creado_en', 'categoria', 'estado')
    search_fields = ('titulo', 'detalle')
    list_filter = ('categoria', 'etiquetas', 'autor', 'creado_en')

# Configuración personalizada para el modelo de Comentario
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ('publicacion', 'nombre', 'creado_en')
    list_filter = ('creado_en', 'publicacion')
    search_fields = ('nombre', 'cuerpo')

# Configuración personalizada para el modelo de Etiqueta
class EtiquetaAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('nombre',)}

# Registro de los modelos en el admin con clases personalizadas
admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(Blog, BlogAdmin)
admin.site.register(Autor, AutorAdmin)
admin.site.register(Comentario, ComentarioAdmin)
admin.site.register(Respuesta)
admin.site.register(Etiqueta, EtiquetaAdmin)
admin.site.register(RegistroCorreo)
admin.site.register(Contacto)
