"""
app_gastronomia/urls.py - Configuración de URLs de la aplicación de gastronomía.

Define las rutas para vistas públicas y CRUD de platos típicos.
"""

from django.urls import path
from . import views

urlpatterns = [
    # ============================================================
    # Vistas públicas (informativas)
    # ============================================================
    # Vista de presentación de gastronomía → /gastronomia/
    path('', views.inicio_gastronomia, name='gastronomia_inicio'),

    # Vista de listado de platos → /gastronomia/platos/
    path('platos/', views.platos_tipicos, name='gastronomia_platos'),

    # Vista de detalle de un plato → /gastronomia/plato/1/
    path('plato/<int:plato_id>/', views.detalle_plato, name='gastronomia_detalle'),

    # ============================================================
    # CRUD Mantenedor de Platos Típicos
    # ============================================================
    path('gestion/platos/', views.plato_lista, name='gastronomia_plato_lista'),
    path('gestion/platos/crear/', views.plato_crear, name='gastronomia_plato_crear'),
    path('gestion/platos/<int:plato_id>/editar/', views.plato_editar, name='gastronomia_plato_editar'),
    path('gestion/platos/<int:plato_id>/eliminar/', views.plato_eliminar, name='gastronomia_plato_eliminar'),
]
