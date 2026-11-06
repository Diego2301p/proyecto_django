"""
app_turismo/urls.py - Configuración de URLs de la aplicación de turismo.

Define las rutas para vistas públicas, CRUD de destinos y reservas turísticas.
"""

from django.urls import path
from . import views

urlpatterns = [
    # ============================================================
    # Vistas públicas (informativas)
    # ============================================================
    # Vista de inicio/presentación → /turismo/
    path('', views.inicio, name='turismo_inicio'),

    # Vista de listado de destinos → /turismo/destinos/
    path('destinos/', views.destinos, name='turismo_destinos'),

    # Vista de detalle de un destino → /turismo/destino/1/
    path('destino/<int:destino_id>/', views.detalle_destino, name='turismo_detalle'),

    # ============================================================
    # CRUD Mantenedor de Destinos Turísticos
    # ============================================================
    path('gestion/destinos/', views.destino_lista, name='turismo_destino_lista'),
    path('gestion/destinos/crear/', views.destino_crear, name='turismo_destino_crear'),
    path('gestion/destinos/<int:destino_id>/editar/', views.destino_editar, name='turismo_destino_editar'),
    path('gestion/destinos/<int:destino_id>/eliminar/', views.destino_eliminar, name='turismo_destino_eliminar'),

    # ============================================================
    # CRUD Transacción: Reservas Turísticas
    # ============================================================
    path('gestion/reservas/', views.reserva_lista, name='turismo_reserva_lista'),
    path('gestion/reservas/crear/', views.reserva_crear, name='turismo_reserva_crear'),
    path('gestion/reservas/<int:reserva_id>/', views.reserva_detalle, name='turismo_reserva_detalle'),
    path('gestion/reservas/<int:reserva_id>/editar/', views.reserva_editar, name='turismo_reserva_editar'),
    path('gestion/reservas/<int:reserva_id>/eliminar/', views.reserva_eliminar, name='turismo_reserva_eliminar'),
]
