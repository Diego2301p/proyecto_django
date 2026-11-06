"""
Management command: crear_roles

Crea los tres perfiles (grupos) exigidos por la evaluación y les asigna
permisos diferenciados del sistema de permisos de Django:

    Administrador  → Acceso total (todos los permisos de mantenedores,
                     transacciones y usuarios).
    Supervisor     → Permisos intermedios (agregar/ver/modificar destinos,
                     platos y reservas; sin eliminar, sin usuarios).
    Administrativo → Permisos mínimos (ver destinos/platos, ver y agregar
                     reservas).

Opcionalmente crea un usuario de demostración por perfil.

Uso:
    python manage.py crear_roles
    python manage.py crear_roles --usuarios-demo
"""

from django.contrib.auth.models import Group, Permission, User
from django.core.management.base import BaseCommand


# Permisos por perfil: (app_label, codename)
PERMISOS = {
    'Administrador': [
        ('app_turismo', 'add_destinoturistico'), ('app_turismo', 'view_destinoturistico'),
        ('app_turismo', 'change_destinoturistico'), ('app_turismo', 'delete_destinoturistico'),
        ('app_gastronomia', 'add_platotipico'), ('app_gastronomia', 'view_platotipico'),
        ('app_gastronomia', 'change_platotipico'), ('app_gastronomia', 'delete_platotipico'),
        ('app_turismo', 'add_reservaturistica'), ('app_turismo', 'view_reservaturistica'),
        ('app_turismo', 'change_reservaturistica'), ('app_turismo', 'delete_reservaturistica'),
        ('auth', 'add_user'), ('auth', 'view_user'), ('auth', 'change_user'), ('auth', 'delete_user'),
    ],
    'Supervisor': [
        ('app_turismo', 'add_destinoturistico'), ('app_turismo', 'view_destinoturistico'),
        ('app_turismo', 'change_destinoturistico'),
        ('app_gastronomia', 'add_platotipico'), ('app_gastronomia', 'view_platotipico'),
        ('app_gastronomia', 'change_platotipico'),
        ('app_turismo', 'add_reservaturistica'), ('app_turismo', 'view_reservaturistica'),
        ('app_turismo', 'change_reservaturistica'),
    ],
    'Administrativo': [
        ('app_turismo', 'view_destinoturistico'),
        ('app_gastronomia', 'view_platotipico'),
        ('app_turismo', 'add_reservaturistica'), ('app_turismo', 'view_reservaturistica'),
    ],
}

# Usuarios de demostración: (username, nombre, apellido, email, grupo)
USUARIOS_DEMO = [
    ('admin', 'Ana', 'Administradora', 'admin@chiledescubre.cl', 'Administrador'),
    ('supervisor', 'Sergio', 'Supervisor', 'supervisor@chiledescubre.cl', 'Supervisor'),
    ('administrativo', 'Andrea', 'Administrativa', 'administrativo@chiledescubre.cl', 'Administrativo'),
]
PASSWORD_DEMO = 'Dark2301$'


class Command(BaseCommand):
    help = 'Crea los perfiles Administrador, Supervisor y Administrativo con sus permisos.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--usuarios-demo', action='store_true',
            help=f'Crea un usuario de prueba por perfil (contraseña: {PASSWORD_DEMO}).'
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE('=== Configurando perfiles y permisos ==='))

        for nombre_grupo, permisos in PERMISOS.items():
            grupo, creado = Group.objects.get_or_create(name=nombre_grupo)
            objetos = []
            for app_label, codename in permisos:
                try:
                    objetos.append(Permission.objects.get(
                        content_type__app_label=app_label, codename=codename
                    ))
                except Permission.DoesNotExist:
                    self.stdout.write(self.style.WARNING(
                        f'  ! Permiso no encontrado: {app_label}.{codename} (¿ejecutaste migrate?)'
                    ))
            grupo.permissions.set(objetos)
            estado = 'creado' if creado else 'actualizado'
            self.stdout.write(f'  ✓ Grupo "{nombre_grupo}" {estado} con {len(objetos)} permisos.')

        if options['usuarios_demo']:
            self.stdout.write(self.style.NOTICE('=== Creando usuarios de demostración ==='))
            for username, nombre, apellido, email, nombre_grupo in USUARIOS_DEMO:
                user, creado = User.objects.get_or_create(
                    username=username,
                    defaults={'first_name': nombre, 'last_name': apellido, 'email': email},
                )
                user.set_password(PASSWORD_DEMO)
                user.save()
                user.groups.set([Group.objects.get(name=nombre_grupo)])
                estado = 'creado' if creado else 'actualizado'
                self.stdout.write(f'  ✓ {username} [{nombre_grupo}] {estado}')
            self.stdout.write(self.style.WARNING(
                f'Contraseña asignada a los usuarios demo: {PASSWORD_DEMO}'
            ))

        self.stdout.write(self.style.SUCCESS('=== Perfiles configurados correctamente ==='))

