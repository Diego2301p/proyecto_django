"""
config/urls.py - Archivo de URLs principal del proyecto.

Actúa como punto de entrada único del proyecto. Usa include() para
vincular las rutas de cada aplicación bajo su propio prefijo:
- /             → Redirige al inicio de app_turismo
- /accounts/    → Login, logout, dashboards y gestión de usuarios
- /password-reset/ → Recuperación de contraseña por correo electrónico
- /turismo/     → Rutas de la aplicación de turismo
- /gastronomia/ → Rutas de la aplicación de gastronomía

Evaluación Sumativa 3: se elimina la ruta /admin/. Toda la gestión
se realiza desde interfaces propias desarrolladas con Django Templates.
"""

from django.urls import path, include, reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth import views as auth_views


def redirigir_a_inicio(request):
    """
    Vista simple que redirige la ruta raíz '/' hacia la página
    de inicio de la aplicación de turismo.
    """
    return redirect('turismo_inicio')


urlpatterns = [
    # Página de inicio general del proyecto → redirige a app_turismo
    path('', redirigir_a_inicio, name='inicio'),

    # Autenticación, dashboards y gestión de usuarios
    path('accounts/', include('accounts.urls')),

    # ============================================================
    # RECUPERACIÓN DE CONTRASEÑA (sistema de autenticación de Django)
    # 1. Solicitar recuperación mediante correo electrónico
    # 2. Generar token seguro (PasswordResetTokenGenerator)
    # 3. Enviar enlace de recuperación al correo del usuario
    # 4. Validar token
    # 5. Establecer nueva contraseña
    # 6. Confirmar cambio exitoso
    # ============================================================
    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='accounts/password_reset_form.html',
             email_template_name='accounts/password_reset_email.txt',
             html_email_template_name='accounts/password_reset_email.html',
             subject_template_name='accounts/password_reset_subject.txt',
             success_url=reverse_lazy('password_reset_done'),
         ),
         name='password_reset'),
    path('password-reset/enviado/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='accounts/password_reset_done.html',
         ),
         name='password_reset_done'),
    path('password-reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='accounts/password_reset_confirm.html',
             success_url=reverse_lazy('password_reset_complete'),
         ),
         name='password_reset_confirm'),
    path('password-reset/completado/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='accounts/password_reset_complete.html',
         ),
         name='password_reset_complete'),

    # Rutas de la aplicación de destinos turísticos de Chile
    path('turismo/', include('app_turismo.urls')),

    # Rutas de la aplicación de platos típicos chilenos
    path('gastronomia/', include('app_gastronomia.urls')),
]
