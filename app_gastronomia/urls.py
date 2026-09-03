"""
app_gastronomia/urls.py - Configuración de URLs de la aplicación de gastronomía.

Define las rutas específicas de esta aplicación, que se incluyen
en el urls.py principal bajo el prefijo 'gastronomia/'.
"""

from django.urls import path
from . import views

urlpatterns = [
    # Vista de presentación de gastronomía → /gastronomia/
    path('', views.inicio_gastronomia, name='gastronomia_inicio'),

    # Vista de listado de platos → /gastronomia/platos/
    path('platos/', views.platos_tipicos, name='gastronomia_platos'),

    # Vista de detalle de un plato → /gastronomia/plato/1/
    path('plato/<int:plato_id>/', views.detalle_plato, name='gastronomia_detalle'),
]
