"""
accounts/views.py - Vistas de autenticación, dashboards y gestión de usuarios.

Implementa:
- Login y logout.
- Dashboard diferenciado por perfil (Administrador, Supervisor, Administrativo).
- CRUD de usuarios (solo Administrador).
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.db.models import Q
from django.utils.http import url_has_allowed_host_and_scheme

from .forms import LoginForm, UsuarioCrearForm, UsuarioEditarForm
from .decorators import grupo_requerido

from app_turismo.models import DestinoTuristico, ReservaTuristica
from app_gastronomia.models import PlatoTipico


# ============================================================
# FUNCIONES AUXILIARES
# ============================================================

def obtener_grupo_usuario(user):
    """Retorna el nombre del grupo principal del usuario."""
    grupos = user.groups.all()
    if grupos.exists():
        return grupos.first().name
    return None


# ============================================================
# AUTENTICACIÓN
# ============================================================

def login_view(request):
    """
    Vista de inicio de sesión.
    Si el usuario ya está autenticado, redirige al dashboard.
    """
    if request.user.is_authenticated:
        return redirect('accounts_dashboard')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    messages.success(
                        request,
                        f'¡Bienvenido, {user.get_full_name() or user.username}!'
                    )
                    # Respetar ?next= solo si es una URL segura del propio sitio
                    siguiente = request.POST.get('next') or request.GET.get('next')
                    if siguiente and url_has_allowed_host_and_scheme(
                        siguiente, allowed_hosts={request.get_host()},
                        require_https=request.is_secure()
                    ):
                        return redirect(siguiente)
                    return redirect('accounts_dashboard')
                else:
                    messages.error(request, 'Tu cuenta está desactivada.')
            else:
                messages.error(request, 'Usuario o contraseña incorrectos.')
    else:
        form = LoginForm()

    return render(request, 'accounts/login.html', {
        'form': form,
        'titulo': 'Iniciar Sesión'
    })


@login_required(login_url='accounts_login')
def logout_view(request):
    """Cierra la sesión del usuario y redirige al login."""
    logout(request)
    messages.info(request, 'Has cerrado sesión correctamente.')
    return redirect('accounts_login')


# ============================================================
# DASHBOARD - REDIRECCIÓN POR PERFIL
# ============================================================

@login_required(login_url='accounts_login')
def dashboard(request):
    """
    Redirige al dashboard correspondiente según el perfil del usuario.
    """
    grupo = obtener_grupo_usuario(request.user)
    if request.user.is_superuser or grupo == 'Administrador':
        return redirect('accounts_dashboard_admin')
    elif grupo == 'Supervisor':
        return redirect('accounts_dashboard_supervisor')
    else:
        return redirect('accounts_dashboard_administrativo')


@grupo_requerido('Administrador')
def dashboard_admin(request):
    """
    Dashboard del Administrador.
    Acceso total: todos los mantenedores, transacciones y gestión de usuarios.
    """
    # Estadísticas generales
    total_destinos = DestinoTuristico.objects.count()
    total_platos = PlatoTipico.objects.count()
    total_reservas = ReservaTuristica.objects.count()
    total_usuarios = User.objects.count()
    reservas_pendientes = ReservaTuristica.objects.filter(estado='Pendiente').count()
    reservas_recientes = ReservaTuristica.objects.select_related(
        'usuario', 'destino', 'plato'
    ).order_by('-created_at')[:5]

    contexto = {
        'titulo': 'Dashboard Administrador',
        'total_destinos': total_destinos,
        'total_platos': total_platos,
        'total_reservas': total_reservas,
        'total_usuarios': total_usuarios,
        'reservas_pendientes': reservas_pendientes,
        'reservas_recientes': reservas_recientes,
        'grupo': 'Administrador',
    }
    return render(request, 'accounts/dashboard_admin.html', contexto)


@grupo_requerido('Supervisor')
def dashboard_supervisor(request):
    """
    Dashboard del Supervisor.
    Acceso a mantenedores autorizados y transacciones.
    Sin gestión de usuarios.
    """
    total_destinos = DestinoTuristico.objects.count()
    total_platos = PlatoTipico.objects.count()
    total_reservas = ReservaTuristica.objects.count()
    reservas_pendientes = ReservaTuristica.objects.filter(estado='Pendiente').count()
    reservas_recientes = ReservaTuristica.objects.select_related(
        'usuario', 'destino', 'plato'
    ).order_by('-created_at')[:5]

    contexto = {
        'titulo': 'Dashboard Supervisor',
        'total_destinos': total_destinos,
        'total_platos': total_platos,
        'total_reservas': total_reservas,
        'reservas_pendientes': reservas_pendientes,
        'reservas_recientes': reservas_recientes,
        'grupo': 'Supervisor',
    }
    return render(request, 'accounts/dashboard_supervisor.html', contexto)


@grupo_requerido('Administrativo')
def dashboard_administrativo(request):
    """
    Dashboard del Administrativo.
    Acceso únicamente a funcionalidades asignadas.
    Restricción de operaciones críticas.
    """
    # Solo ve las reservas (no puede gestionar mantenedores)
    total_reservas = ReservaTuristica.objects.count()
    reservas_pendientes = ReservaTuristica.objects.filter(estado='Pendiente').count()
    total_destinos = DestinoTuristico.objects.count()
    total_platos = PlatoTipico.objects.count()

    contexto = {
        'titulo': 'Dashboard Administrativo',
        'total_reservas': total_reservas,
        'reservas_pendientes': reservas_pendientes,
        'total_destinos': total_destinos,
        'total_platos': total_platos,
        'grupo': 'Administrativo',
    }
    return render(request, 'accounts/dashboard_administrativo.html', contexto)


# ============================================================
# GESTIÓN DE USUARIOS (Solo Administrador)
# ============================================================

@grupo_requerido('Administrador')
def usuario_lista(request):
    """Lista todos los usuarios del sistema con búsqueda."""
    query = request.GET.get('q', '')
    if query:
        usuarios = User.objects.filter(
            Q(username__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(email__icontains=query)
        ).order_by('username')
    else:
        usuarios = User.objects.all().order_by('username')

    # Agregar info de grupo a cada usuario
    usuarios_con_grupo = []
    for usuario in usuarios:
        grupos = usuario.groups.all()
        grupo_nombre = grupos.first().name if grupos.exists() else 'Sin grupo'
        usuarios_con_grupo.append({
            'user': usuario,
            'grupo': grupo_nombre,
        })

    contexto = {
        'titulo': 'Gestión de Usuarios',
        'usuarios': usuarios_con_grupo,
        'query': query,
        'total': len(usuarios_con_grupo),
    }
    return render(request, 'accounts/usuario_lista.html', contexto)


@grupo_requerido('Administrador')
def usuario_crear(request):
    """Crea un nuevo usuario con asignación de grupo."""
    if request.method == 'POST':
        form = UsuarioCrearForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(
                request,
                f'Usuario "{user.username}" creado exitosamente.'
            )
            return redirect('accounts_usuario_lista')
    else:
        form = UsuarioCrearForm()

    contexto = {
        'titulo': 'Crear Usuario',
        'form': form,
    }
    return render(request, 'accounts/usuario_form.html', contexto)


@grupo_requerido('Administrador')
def usuario_editar(request, user_id):
    """Edita un usuario existente."""
    usuario = get_object_or_404(User, pk=user_id)
    if request.method == 'POST':
        form = UsuarioEditarForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                f'Usuario "{usuario.username}" actualizado exitosamente.'
            )
            return redirect('accounts_usuario_lista')
    else:
        form = UsuarioEditarForm(instance=usuario)

    contexto = {
        'titulo': f'Editar Usuario: {usuario.username}',
        'form': form,
        'usuario_editado': usuario,
    }
    return render(request, 'accounts/usuario_form.html', contexto)


@grupo_requerido('Administrador')
def usuario_eliminar(request, user_id):
    """Elimina un usuario del sistema."""
    usuario = get_object_or_404(User, pk=user_id)
    if request.method == 'POST':
        nombre = usuario.username
        usuario.delete()
        messages.success(request, f'Usuario "{nombre}" eliminado exitosamente.')
        return redirect('accounts_usuario_lista')

    contexto = {
        'titulo': f'Eliminar Usuario: {usuario.username}',
        'usuario_eliminar': usuario,
    }
    return render(request, 'accounts/usuario_eliminar.html', contexto)

