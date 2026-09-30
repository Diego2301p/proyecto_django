"""
app_gastronomia/admin.py - Registro de modelos en Django Admin.

Registra el modelo PlatoTipico para poder crear, editar y
eliminar platos típicos desde el panel de administración
de Django (Requisito: Django Admin operativo con registros
creados/editados/eliminados).
"""

from django.contrib import admin
from .models import PlatoTipico


@admin.register(PlatoTipico)
class PlatoTipicoAdmin(admin.ModelAdmin):
    """Configuración del modelo PlatoTipico en el admin."""
    list_display = ('id', 'nombre', 'region', 'dificultad', 'tiempo_preparacion', 'precio_referencia', 'es_vegetariano')
    list_filter = ('dificultad', 'es_vegetariano', 'region')
    search_fields = ('nombre', 'region', 'descripcion', 'ingredientes')
    list_editable = ('es_vegetariano',)
    ordering = ('id',)
