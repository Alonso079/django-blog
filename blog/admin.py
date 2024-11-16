from django.contrib import admin
from .models import Autor, Categoria, Blog, Etiqueta, RegistroCorreo, Contacto, Comentario, Respuesta

# Configuración personalizada para el modelo de Autor
class AutorAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'correo', 'nombre', 'apellido', 'cargo', 'estado_autor')
    search_fields = ('usuario__username', 'nombre', 'apellido', 'correo')
    list_filter = ('cargo', 'estado_autor')
    ordering = ('usuario',)

# Configuración personalizada para el modelo de Categoría
class CategoriaAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('nombre',)}
    list_display = ('nombre', 'slug', 'descripcion')
    search_fields = ('nombre', 'descripcion')

# Configuración personalizada para el modelo de Blog
class BlogAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'autor', 'creado_en', 'categoria', 'estado', 'visible', 'destacado')
    search_fields = ('titulo', 'detalle', 'autor__usuario__username')
    list_filter = ('categoria', 'etiquetas', 'autor', 'estado', 'visible', 'destacado', 'creado_en')
    ordering = ('-creado_en',)
    autocomplete_fields = ['autor', 'categoria', 'etiquetas']
    readonly_fields = ('conteo_visitas',)

    def get_queryset(self, request):
        # Filtrar para mostrar solo los blogs que están visibles y activos
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            return qs.filter(visible=True, estado='activo')
        return qs

    def has_view_permission(self, request, obj=None):
        # Permitir que los usuarios vean el blog si tienen permisos
        if request.user.is_superuser or request.user.has_perm('blog.view_blog'):
            return True
        return False

    def has_change_permission(self, request, obj=None):
        # Permitir la edición solo a los usuarios con permisos específicos
        if request.user.is_superuser or request.user.has_perm('blog.change_blog'):
            return True
        return False

# Configuración personalizada para el modelo de Comentario
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ('publicacion', 'nombre', 'creado_en', 'estado')
    list_filter = ('creado_en', 'publicacion', 'estado')
    search_fields = ('nombre', 'cuerpo', 'publicacion__titulo')
    ordering = ('-creado_en',)

# Configuración personalizada para el modelo de Respuesta
class RespuestaAdmin(admin.ModelAdmin):
    list_display = ('comentario', 'nombre', 'creado_en')
    search_fields = ('comentario__cuerpo', 'nombre', 'cuerpo')
    list_filter = ('creado_en',)
    ordering = ('-creado_en',)

# Configuración personalizada para el modelo de Etiqueta
class EtiquetaAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('nombre',)}
    list_display = ('nombre', 'slug', 'descripcion')
    search_fields = ('nombre', 'descripcion')
    ordering = ('nombre',)

# Configuración personalizada para el modelo de RegistroCorreo
class RegistroCorreoAdmin(admin.ModelAdmin):
    list_display = ('correo', 'creado_en')
    search_fields = ('correo',)
    ordering = ('-creado_en',)

# Configuración personalizada para el modelo de Contacto
class ContactoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'correo', 'asunto', 'mensaje')
    search_fields = ('nombre', 'correo', 'asunto', 'mensaje')
    ordering = ('-nombre',)

# Registro de los modelos en el admin con clases personalizadas
models_to_register = [
    (Categoria, CategoriaAdmin),
    (Blog, BlogAdmin),
    (Autor, AutorAdmin),
    (Comentario, ComentarioAdmin),
    (Respuesta, RespuestaAdmin),
    (Etiqueta, EtiquetaAdmin),
    (RegistroCorreo, RegistroCorreoAdmin),
    (Contacto, ContactoAdmin)
]

for model, admin_class in models_to_register:
    try:
        admin.site.register(model, admin_class)
    except admin.sites.AlreadyRegistered:
        pass
