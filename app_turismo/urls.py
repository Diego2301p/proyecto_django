"""
app_turismo/urls.py - Configuración de URLs de la aplicación de turismo.

Define las rutas específicas de esta aplicación, que se incluyen
en el urls.py principal bajo el prefijo 'turismo/'.
"""

from django.urls import path
from . import views

# app_name permite usar namespaces en las URLs (ej: {% url 'turismo_inicio' %})
urlpatterns = [
    # Vista de inicio/presentación → /turismo/
    path('', views.inicio, name='turismo_inicio'),

    # Vista de listado de destinos → /turismo/destinos/
    path('destinos/', views.destinos, name='turismo_destinos'),

    # Vista de detalle de un destino → /turismo/destino/1/
    path('destino/<int:destino_id>/', views.detalle_destino, name='turismo_detalle'),
]
