"""
accounts/urls.py - Configuración de URLs de la app de cuentas.

Define las rutas para autenticación, dashboards y gestión de usuarios.
"""

from django.urls import path
from . import views

urlpatterns = [
    # Autenticación
    path('login/', views.login_view, name='accounts_login'),
    path('logout/', views.logout_view, name='accounts_logout'),

    # Dashboard (redirige según perfil)
    path('dashboard/', views.dashboard, name='accounts_dashboard'),
    path('dashboard/admin/', views.dashboard_admin, name='accounts_dashboard_admin'),
    path('dashboard/supervisor/', views.dashboard_supervisor, name='accounts_dashboard_supervisor'),
    path('dashboard/administrativo/', views.dashboard_administrativo, name='accounts_dashboard_administrativo'),

    # Gestión de usuarios (solo Administrador)
    path('usuarios/', views.usuario_lista, name='accounts_usuario_lista'),
    path('usuarios/crear/', views.usuario_crear, name='accounts_usuario_crear'),
    path('usuarios/<int:user_id>/editar/', views.usuario_editar, name='accounts_usuario_editar'),
    path('usuarios/<int:user_id>/eliminar/', views.usuario_eliminar, name='accounts_usuario_eliminar'),
]

