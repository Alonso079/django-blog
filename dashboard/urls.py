
from django.urls import path
from . import views

urlpatterns = [
    # Dashboard de Usuario
    path('', views.Dashboard.as_view(), name='dashboard'),

    # Publicaciones
    path('crear-publicacion/', views.CrearPublicacion.as_view(), name='crear_publicacion'),
    path('publicaciones/', views.ListarPublicaciones.as_view(), name='todas_publicaciones'),
    path('publicacion/ver/<str:id>/', views.VerPublicacion.as_view(), name='ver_publicacion'),
    path('publicacion/editar/<str:id>/', views.EditarPublicacion.as_view(), name='editar_publicacion'),
    path('publicacion/eliminar/<str:id>/', views.EliminarPublicacion.as_view(), name='eliminar_publicacion'),
    path('publicaciones-activas/', views.ListarPublicacionesActivas.as_view(), name='publicaciones_activas'),
    path('publicaciones-pendientes/', views.ListarPublicacionesPendientes.as_view(), name='publicaciones_pendientes'),
    path('publicacion/visible/<str:id>/', views.HacerPublicacionVisible.as_view(), name='publicacion_visible'),
    path('publicacion/ocultar/<str:id>/', views.OcultarPublicacion.as_view(), name='ocultar_publicacion'),
    path('dashboard/crear-publicacion-usuario/', views.CrearPublicacionUser.as_view(), name='crear_publicacion_usuario'),


    # Autor
    path('perfil/', views.PerfilAutor.as_view(), name='perfil'),
    path('perfil/editar/', views.EditarAutor.as_view(), name='editar_perfil'),

    # Categoría
    path('categorias/', views.ListarCategorias.as_view(), name='categorias'),
    path('agregar-categoria/', views.CrearCategoria.as_view(), name='agregar_categoria'),
    path('editar-categoria/<str:id>/', views.ActualizarCategoria.as_view(), name='editar_categoria'),
    path('eliminar-categoria/<str:id>/', views.EliminarCategoria.as_view(), name='eliminar_categoria'),

    # Etiqueta
    path('etiquetas/', views.ListarEtiquetas.as_view(), name='etiquetas'),
    path('agregar-etiqueta/', views.CrearEtiqueta.as_view(), name='agregar_etiqueta'),
    path('editar-etiqueta/<str:id>/', views.ActualizarEtiqueta.as_view(), name='editar_etiqueta'),
    path('eliminar-etiqueta/<str:id>/', views.EliminarEtiqueta.as_view(), name='eliminar_etiqueta'),

]