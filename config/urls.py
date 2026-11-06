"""
config/urls.py - Archivo de URLs principal del proyecto.

Rutas principales:
- /                -> Redirige al inicio de app_turismo
- /accounts/       -> Login, logout, dashboards y usuarios
- /password-reset/ -> Recuperación de contraseña por correo
- /turismo/        -> Destinos turísticos y reservas
- /gastronomia/    -> Platos típicos chilenos
"""

from django.urls import path, include, reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth import views as auth_views


def redirigir_a_inicio(request):
    return redirect('turismo_inicio')


urlpatterns = [
    path('', redirigir_a_inicio, name='inicio'),
    path('accounts/', include('accounts.urls')),

    # Recuperación de contraseña por correo
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

    path('turismo/', include('app_turismo.urls')),
    path('gastronomia/', include('app_gastronomia.urls')),
]
