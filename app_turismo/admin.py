"""
app_turismo/admin.py - Registro de modelos en Django Admin.

Registra el modelo DestinoTuristico para poder crear, editar y
eliminar destinos turísticos desde el panel de administración
de Django (Requisito: Django Admin operativo con registros
creados/editados/eliminados).
"""

from django.contrib import admin
from .models import DestinoTuristico


@admin.register(DestinoTuristico)
class DestinoTuristicoAdmin(admin.ModelAdmin):
    """Configuración del modelo DestinoTuristico en el admin."""
    list_display = ('id', 'nombre', 'region', 'categoria', 'precio_estimado', 'puntuacion', 'destacado')
    list_filter = ('categoria', 'destacado', 'region')
    search_fields = ('nombre', 'region', 'descripcion')
    list_editable = ('destacado',)
    ordering = ('id',)
