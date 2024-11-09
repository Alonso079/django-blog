from django.urls import path
from . import views

urlpatterns = [
    path('', views.BuscarView.as_view(), name='home'),  # Página principal del blog
    path('blog/<int:id>/', views.VerPublicacion.as_view(), name='ver_publicacion'),  # Vista individual de un blog
    path('categoria/<slug:slug>/', views.CategoriaView.as_view(), name='categoria'),  # Vista de categorías
    path('etiqueta/<int:id>/', views.EtiquetaView.as_view(), name='etiqueta'),  # Vista por etiquetas
    path('suscribir/', views.SubscripcionView.as_view(), name='suscribir'),  # Suscripción
    path('buscar/', views.BuscarView.as_view(), name='buscar'),  # Buscar en el blog
    path('<int:id>/crear-comentario/', views.ComentarioView.as_view(), name='crear_comentario'),  # Crear comentario en un blog

    # Vista de prueba
    path('prueba/', views.PruebaView, name='prueba'),
    
    # Listar etiquetas
    path('etiquetas/', views.ListarEtiquetasView.as_view(), name='listar_etiquetas'),
]
