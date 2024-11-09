"""
Configuración de Django para el proyecto src.

Generado por 'django-admin startproject' usando Django 5.1.1.

Para más información sobre este archivo, consulta
https://docs.djangoproject.com/en/5.1/topics/settings/

Para la lista completa de configuraciones y sus valores, consulta
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
import os

# Construir rutas dentro del proyecto, como BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Configuraciones de desarrollo - no apto para producción
# Ver https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# ADVERTENCIA DE SEGURIDAD: mantener la clave secreta en producción segura
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'clave-secreta-defecto')

# ADVERTENCIA DE SEGURIDAD: no ejecutar con debug activado en producción
DEBUG = os.getenv('DJANGO_DEBUG', 'False') == 'True'

ALLOWED_HOSTS = os.getenv('DJANGO_ALLOWED_HOSTS', '').split(',')

# Definición de aplicaciones
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Aplicaciones adicionales
    'rest_framework',
    'django.contrib.humanize',
    'blog',
    'dashboard',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'src.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'src.wsgi.application'

# Base de datos
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases
import pymysql
pymysql.install_as_MySQLdb()
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('POSTGRES_DB', 'django'),  # Nombre de la base de datos por defecto
        'USER': os.getenv('POSTGRES_USER', 'diogenes'),  # Usuario de la base de datos
        'PASSWORD': os.getenv('POSTGRES_PASSWORD', 'Cfwt6593@1'),  # Contraseña de la base de datos
        'HOST': os.getenv('POSTGRES_HOST', '192.168.100.58'),  # Host de la base de datos
        'PORT': os.getenv('POSTGRES_PORT', '3306'),  # Puerto por defecto de PostgreSQL
    }
}
# Validación de contraseñas
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internacionalización
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'es-cl'

TIME_ZONE = 'America/Santiago'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Archivos estáticos (CSS, Imágenes)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'imagenes/')

# Tipo de campo de clave primaria predeterminado
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

DEBUG = True

ALLOWED_HOSTS = ['*']
