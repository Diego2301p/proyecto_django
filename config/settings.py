"""
Django settings for config project.
Proyecto: Chile Descubre - Sitio informativo sobre turismo y gastronomía chilena.

Se eliminaron las dependencias de base de datos (admin, auth, sessions, contenttypes)
para cumplir con el requisito de NO usar base de datos.
Los datos se almacenan en archivos JSON dentro de cada aplicación.
"""

from pathlib import Path
import os

# ============================================================
# RUTAS BASE DEL PROYECTO
# ============================================================
# BASE_DIR apunta a la carpeta raíz del proyecto (proyecto_django/)
BASE_DIR = Path(__file__).resolve().parent.parent


# ============================================================
# SEGURIDAD
# ============================================================
# Clave secreta para desarrollo local (NO usar en producción)
SECRET_KEY = 'django-insecure-aqm$ti%ux8%p5g7v0c@zxa2!v@7%@ddp@tx-s$rly+y=c_b3x-'

# Modo debug activado para desarrollo local
DEBUG = True

# Hosts permitidos (vacío permite localhost en modo DEBUG)
ALLOWED_HOSTS = []


# ============================================================
# APLICACIONES INSTALADAS
# ============================================================
# Solo se incluyen las apps estrictamente necesarias para un proyecto
# sin base de datos: staticfiles (para servir CSS/JS/imágenes) y
# las dos apps propias del proyecto.
INSTALLED_APPS = [
    'django.contrib.staticfiles',  # Necesario para {% static %} en templates
    'app_turismo',                 # App de destinos turísticos de Chile
    'app_gastronomia',             # App de platos típicos chilenos
]


# ============================================================
# MIDDLEWARE
# ============================================================
# Se eliminaron los middleware de sesión, autenticación y mensajes
# ya que no usamos base de datos ni sistema de usuarios.
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# ============================================================
# CONFIGURACIÓN DE URLS
# ============================================================
ROOT_URLCONF = 'config.urls'


# ============================================================
# CONFIGURACIÓN DE PLANTILLAS (TEMPLATES)
# ============================================================
# Se agrega la carpeta 'templates/' a nivel de proyecto en DIRS
# para que Django encuentre base.html y otras plantillas globales.
# APP_DIRS=True permite que Django busque también dentro de
# cada app en <app>/templates/<app>/.
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # Carpeta global de plantillas
        'APP_DIRS': True,                   # Busca en templates/ de cada app
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.template.context_processors.static',  # Para usar STATIC_URL en templates
            ],
        },
    },
]


# ============================================================
# WSGI
# ============================================================
WSGI_APPLICATION = 'config.wsgi.application'


# ============================================================
# BASE DE DATOS - DESHABILITADA
# ============================================================
# Este proyecto NO usa base de datos. Los datos se leen desde
# archivos JSON. Se deja DATABASES vacío para evitar cualquier
# dependencia con SQLite u otro motor.
DATABASES = {}


# ============================================================
# INTERNACIONALIZACIÓN
# ============================================================
LANGUAGE_CODE = 'es-cl'    # Español de Chile
TIME_ZONE = 'America/Santiago'
USE_I18N = True
USE_TZ = True


# ============================================================
# ARCHIVOS ESTÁTICOS (CSS, JavaScript, Imágenes)
# ============================================================
# URL bajo la cual se sirven los archivos estáticos
STATIC_URL = '/static/'

# Carpetas adicionales donde Django buscará archivos estáticos
# (además de las carpetas static/ dentro de cada app)
STATICFILES_DIRS = [
    BASE_DIR / 'static',  # Carpeta estática global del proyecto
]

# Carpeta donde collectstatic recopila todos los estáticos para producción
STATIC_ROOT = BASE_DIR / 'staticfiles'


# ============================================================
# CONFIGURACIÓN POR DEFECTO DE CLAVES PRIMARIAS
# ============================================================
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
