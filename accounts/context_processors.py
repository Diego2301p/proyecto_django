"""
accounts/context_processors.py - Variables de perfil disponibles en todos los templates.

Permite que base.html muestre u oculte opciones de menú según el
perfil (grupo) del usuario autenticado.
"""


def perfil_usuario(request):
    """Agrega al contexto el perfil del usuario y banderas por rol."""
    user = getattr(request, 'user', None)
    if user is None or not user.is_authenticated:
        return {}

    grupos = set(user.groups.values_list('name', flat=True))
    es_admin = user.is_superuser or 'Administrador' in grupos
    es_supervisor = 'Supervisor' in grupos
    es_administrativo = 'Administrativo' in grupos

    if es_admin:
        perfil = 'Administrador'
    elif es_supervisor:
        perfil = 'Supervisor'
    elif es_administrativo:
        perfil = 'Administrativo'
    else:
        perfil = 'Sin perfil'

    return {
        'perfil': perfil,
        'es_admin': es_admin,
        'es_supervisor': es_supervisor,
        'es_administrativo': es_administrativo,
        # Puede gestionar mantenedores (Destinos / Platos)
        'puede_mantenedores': es_admin or es_supervisor,
    }

