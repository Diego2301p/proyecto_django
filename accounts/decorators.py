"""
accounts/decorators.py - Decoradores personalizados para control de acceso.

Proporciona decoradores que restringen el acceso a las vistas según
el grupo (perfil) del usuario autenticado.
"""

from functools import wraps

from django.contrib.auth.decorators import login_required
from django.shortcuts import render


def grupo_requerido(*grupos_permitidos):
    """
    Decorador que restringe el acceso a una vista según el grupo del usuario.
    Solo permite el acceso si el usuario pertenece a alguno de los grupos
    indicados o si es superusuario. Si el usuario no ha iniciado sesión,
    se le redirige al login.

    Uso:
        @grupo_requerido('Administrador')
        def mi_vista(request):
            ...

        @grupo_requerido('Administrador', 'Supervisor')
        def otra_vista(request):
            ...
    """
    def decorator(view_func):
        @wraps(view_func)
        @login_required(login_url='accounts_login')
        def wrapper(request, *args, **kwargs):
            # Los superusuarios siempre tienen acceso total
            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)
            # Verificar si el usuario pertenece a alguno de los grupos permitidos
            if request.user.groups.filter(name__in=grupos_permitidos).exists():
                return view_func(request, *args, **kwargs)
            # Si no tiene permisos, mostrar página 403 (acceso denegado)
            return render(request, 'accounts/403.html', {
                'titulo': 'Acceso denegado',
                'grupos_permitidos': grupos_permitidos,
            }, status=403)
        return wrapper
    return decorator
