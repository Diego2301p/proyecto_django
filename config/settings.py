"""
Django settings for config project.
Proyecto: Chile Descubre - Sitio informativo sobre turismo y gastronomía chilena.

Migrado a Django ORM con MySQL como motor de base de datos.
Se habilitan las apps de admin, auth, sessions y contenttypes
para poder usar el panel de administración de Django.
Las variables sensibles se leen desde un archivo .env usando python-dotenv.
"""

from pathlib import Path
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()

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

# Hosts permitidos: incluir la IP fija de EC2 al desplegar
# Ejemplo: ALLOWED_HOSTS = ['<TU_IP_FIJA>', 'localhost', '127.0.0.1']
ALLOWED_HOSTS = ['*']


# ============================================================
# APLICACIONES INSTALADAS
# ============================================================
# Se incluyen las apps de Django necesarias para admin, auth y
# el sistema de contenidos, además de las apps propias.
INSTALLED_APPS = [
    'django.contrib.admin',         # Panel de administración de Django
    'django.contrib.auth',          # Sistema de autenticación
    'django.contrib.contenttypes',  # Framework de tipos de contenido
    'django.contrib.sessions',      # Framework de sesiones
    'django.contrib.messages',      # Framework de mensajes
    'django.contrib.staticfiles',   # Necesario para {% static %} en templates
    'app_turismo',                  # App de destinos turísticos de Chile
    'app_gastronomia',              # App de platos típicos chilenos
]


# ============================================================
# MIDDLEWARE
# ============================================================
# Se incluyen los middleware necesarios para admin, sesiones,
# autenticación y mensajes.
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
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
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
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
# BASE DE DATOS - MySQL
# ============================================================
# Configuración de MySQL usando variables de entorno del archivo .env.
# En EC2: crear la DB, usuario y contraseña según la guía.
DATABASES = {
    'default': {
        'ENGINE': os.getenv('DB_ENGINE', 'django.db.backends.mysql'),
        'NAME': os.getenv('DB_NAME', 'chile_descubre'),
        'USER': os.getenv('DB_USER', 'user_chile'),
        'PASSWORD': os.getenv('DB_PASSWORD', ''),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '3306'),
        'OPTIONS': {
            'charset': 'utf8mb4',
        },
    }
}


# ============================================================
# VALIDACIÓN DE CONTRASEÑAS
# ============================================================
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
