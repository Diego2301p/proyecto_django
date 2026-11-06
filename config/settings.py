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
# Clave secreta leída desde .env (con valor por defecto solo para desarrollo local)
SECRET_KEY = os.getenv(
    'SECRET_KEY',
    'django-insecure-aqm$ti%ux8%p5g7v0c@zxa2!v@7%@ddp@tx-s$rly+y=c_b3x-'
)

# Modo debug controlado por variable de entorno (True por defecto en desarrollo)
DEBUG = os.getenv('DEBUG', 'True') == 'True'

# Hosts permitidos: incluir la IP fija de EC2 al desplegar (separados por coma en .env)
# Ejemplo: ALLOWED_HOSTS=54.12.34.56,localhost,127.0.0.1
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '*').split(',')


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
    'accounts',                     # App de autenticación, perfiles y dashboards
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
                'accounts.context_processors.perfil_usuario',  # Perfil del usuario (roles)
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
DB_ENGINE = os.getenv('DB_ENGINE', 'django.db.backends.mysql')

if DB_ENGINE == 'django.db.backends.sqlite3':
    # Alternativa para pruebas locales sin MySQL (DB_ENGINE=django.db.backends.sqlite3)
    DATABASES = {
        'default': {
            'ENGINE': DB_ENGINE,
            'NAME': BASE_DIR / os.getenv('DB_NAME', 'db.sqlite3'),
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': DB_ENGINE,
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



# ============================================================
# AUTENTICACIÓN Y MENSAJES
# ============================================================
LOGIN_URL = 'accounts_login'
LOGIN_REDIRECT_URL = 'accounts_dashboard'
LOGOUT_REDIRECT_URL = 'accounts_login'

# Mensajes con clases de Bootstrap
from django.contrib.messages import constants as message_constants
MESSAGE_TAGS = {
    message_constants.DEBUG: 'secondary',
    message_constants.INFO: 'info',
    message_constants.SUCCESS: 'success',
    message_constants.WARNING: 'warning',
    message_constants.ERROR: 'danger',
}


# ============================================================
# CORREO ELECTRÓNICO - RECUPERACIÓN DE CONTRASEÑA
# ============================================================
# Por defecto los correos se muestran en la consola (desarrollo).
# Para enviar correos reales (ej: Gmail) definir en .env:
#   EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
#   EMAIL_HOST=smtp.gmail.com
#   EMAIL_PORT=587
#   EMAIL_USE_TLS=True
#   EMAIL_HOST_USER=tu_correo@gmail.com
#   EMAIL_HOST_PASSWORD=contraseña_de_aplicacion_de_16_caracteres
EMAIL_BACKEND = os.getenv('EMAIL_BACKEND', 'django.core.mail.backends.console.EmailBackend')
EMAIL_HOST = os.getenv('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.getenv('EMAIL_PORT', '587'))
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', 'True') == 'True'
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', '')
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', EMAIL_HOST_USER or 'Chile Descubre <no-reply@chiledescubre.cl>')

# Tiempo de validez del token de recuperación (en segundos): 1 hora
PASSWORD_RESET_TIMEOUT = 3600
