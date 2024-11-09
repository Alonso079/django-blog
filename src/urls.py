from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from dashboard import views

urlpatterns = [
    # Administración
    path('admin/', admin.site.urls),

    # Autenticación de usuario
    path('sign-up/', views.CrearAutor.as_view(), name='crear_usuario'),
    path('login/', views.VistaLogin.as_view(), name='login'),
    path('logout/', views.VistaLogout.as_view(), name='logout'),

    # Aplicaciones del proyecto
    path('', include('blog.urls')),  # URLs del blog
    path('dashboard/', include('dashboard.urls')),  # URLs del dashboard

    # Autenticación REST API
    path('api-auth/', include('rest_framework.urls')),
]

# Configuración para servir archivos estáticos y multimedia en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
