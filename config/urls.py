"""
config/urls.py - Archivo de URLs principal del proyecto.

Actúa como punto de entrada único del proyecto. Usa include() para
vincular las rutas de cada aplicación bajo su propio prefijo:
- /            → Redirige al inicio de app_turismo
- /admin/      → Panel de administración de Django
- /turismo/    → Rutas de la aplicación de turismo
- /gastronomia/ → Rutas de la aplicación de gastronomía
"""

from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect


def redirigir_a_inicio(request):
    """
    Vista simple que redirige la ruta raíz '/' hacia la página
    de inicio de la aplicación de turismo.
    """
    return redirect('turismo_inicio')


urlpatterns = [
    # Panel de administración de Django
    path('admin/', admin.site.urls),

    # Página de inicio general del proyecto → redirige a app_turismo
    path('', redirigir_a_inicio, name='inicio'),

    # Rutas de la aplicación de destinos turísticos de Chile
    path('turismo/', include('app_turismo.urls')),

    # Rutas de la aplicación de platos típicos chilenos
    path('gastronomia/', include('app_gastronomia.urls')),
]
