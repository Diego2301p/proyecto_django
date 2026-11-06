"""
accounts/tests.py - Pruebas del módulo de cuentas, permisos y reservas.

Ejecutar con:
    python manage.py test
"""

import io
import re
from datetime import date, timedelta

from django.contrib.auth.models import Group, User
from django.core import mail
from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse

from app_gastronomia.models import PlatoTipico
from app_turismo.models import DestinoTuristico, ReservaTuristica

PASSWORD = 'Dark2301$'


class SistemaTestBase(TestCase):
    """Crea perfiles, un usuario por perfil y datos mínimos."""

    @classmethod
    def setUpTestData(cls):
        call_command('crear_roles', stdout=io.StringIO())
        cls.usuarios = {}
        for username, grupo in [('ana', 'Administrador'), ('sergio', 'Supervisor'), ('andrea', 'Administrativo')]:
            u = User.objects.create_user(username, f'{username}@test.cl', PASSWORD)
            u.groups.add(Group.objects.get(name=grupo))
            cls.usuarios[grupo] = u
        cls.destino = DestinoTuristico.objects.create(
            nombre='Valle del Elqui', region='Coquimbo', descripcion='Valle', imagen='x.jpg',
            categoria='Naturaleza', precio_estimado=30000, puntuacion=4.5)
        cls.plato = PlatoTipico.objects.create(
            nombre='Papayas al jugo', region='Coquimbo', descripcion='Postre', imagen='y.jpg',
            precio_referencia=4000)

    def entrar(self, grupo):
        self.client.login(username=self.usuarios[grupo].username, password=PASSWORD)


class AutenticacionTests(SistemaTestBase):
    def test_login_y_logout(self):
        r = self.client.post(reverse('accounts_login'), {'username': 'ana', 'password': PASSWORD})
        self.assertRedirects(r, reverse('accounts_dashboard'), fetch_redirect_response=False)
        r = self.client.post(reverse('accounts_logout'))
        self.assertRedirects(r, reverse('accounts_login'))
        r = self.client.get(reverse('accounts_dashboard'))
        self.assertEqual(r.status_code, 302)

    def test_login_incorrecto(self):
        r = self.client.post(reverse('accounts_login'), {'username': 'ana', 'password': 'mala'})
        self.assertContains(r, 'Usuario o contraseña incorrectos')

    def test_vistas_protegidas_redirigen_a_login(self):
        for nombre in ['accounts_dashboard', 'turismo_destino_lista', 'gastronomia_plato_lista',
                       'turismo_reserva_lista', 'accounts_usuario_lista']:
            r = self.client.get(reverse(nombre))
            self.assertEqual(r.status_code, 302, nombre)
            self.assertIn(reverse('accounts_login'), r.url)

    def test_admin_de_django_deshabilitado(self):
        self.assertEqual(self.client.get('/admin/').status_code, 404)


class DashboardYPermisosTests(SistemaTestBase):
    def test_dashboard_por_perfil(self):
        esperado = {
            'Administrador': 'accounts_dashboard_admin',
            'Supervisor': 'accounts_dashboard_supervisor',
            'Administrativo': 'accounts_dashboard_administrativo',
        }
        for grupo, url in esperado.items():
            self.entrar(grupo)
            r = self.client.get(reverse('accounts_dashboard'))
            self.assertRedirects(r, reverse(url))
            self.client.logout()

    def test_administrativo_restringido(self):
        self.entrar('Administrativo')
        self.assertEqual(self.client.get(reverse('turismo_destino_lista')).status_code, 403)
        self.assertEqual(self.client.get(reverse('gastronomia_plato_lista')).status_code, 403)
        self.assertEqual(self.client.get(reverse('accounts_usuario_lista')).status_code, 403)
        self.assertEqual(self.client.get(reverse('accounts_dashboard_admin')).status_code, 403)
        self.assertEqual(self.client.get(reverse('turismo_reserva_lista')).status_code, 200)
        self.assertEqual(self.client.get(reverse('turismo_reserva_crear')).status_code, 200)

    def test_supervisor_intermedio(self):
        self.entrar('Supervisor')
        self.assertEqual(self.client.get(reverse('turismo_destino_lista')).status_code, 200)
        self.assertEqual(self.client.get(reverse('turismo_destino_editar', args=[self.destino.id])).status_code, 200)
        self.assertEqual(self.client.get(reverse('turismo_destino_eliminar', args=[self.destino.id])).status_code, 403)
        self.assertEqual(self.client.get(reverse('accounts_usuario_lista')).status_code, 403)

    def test_admin_acceso_total(self):
        self.entrar('Administrador')
        for nombre in ['turismo_destino_lista', 'gastronomia_plato_lista', 'turismo_reserva_lista',
                       'accounts_usuario_lista', 'accounts_usuario_crear']:
            self.assertEqual(self.client.get(reverse(nombre)).status_code, 200, nombre)


class GestionUsuariosTests(SistemaTestBase):
    def test_crear_usuario_con_grupo(self):
        self.entrar('Administrador')
        grupo = Group.objects.get(name='Supervisor')
        r = self.client.post(reverse('accounts_usuario_crear'), {
            'username': 'nuevo', 'first_name': 'Nuevo', 'last_name': 'Usuario',
            'email': 'nuevo@test.cl', 'password1': PASSWORD, 'password2': PASSWORD,
            'grupo': grupo.id,
        })
        self.assertRedirects(r, reverse('accounts_usuario_lista'))
        self.assertTrue(User.objects.get(username='nuevo').groups.filter(name='Supervisor').exists())


class MantenedoresTests(SistemaTestBase):
    def test_crud_destino(self):
        self.entrar('Administrador')
        datos = {'nombre': 'Pisco Elqui', 'region': 'Coquimbo', 'descripcion': 'Pueblo',
                 'imagen': 'p.jpg', 'categoria': 'Cultura', 'precio_estimado': 20000,
                 'puntuacion': 4.2, 'actividades': 'Tour'}
        # Crear
        self.client.post(reverse('turismo_destino_crear'), datos)
        d = DestinoTuristico.objects.get(nombre='Pisco Elqui')
        # Buscar / listar
        r = self.client.get(reverse('turismo_destino_lista'), {'q': 'Pisco'})
        self.assertContains(r, 'Pisco Elqui')
        self.assertNotContains(r, 'Valle del Elqui')
        # Modificar
        datos['nombre'] = 'Pisco Elqui Editado'
        self.client.post(reverse('turismo_destino_editar', args=[d.id]), datos)
        d.refresh_from_db()
        self.assertEqual(d.nombre, 'Pisco Elqui Editado')
        # Eliminar
        self.client.post(reverse('turismo_destino_eliminar', args=[d.id]))
        self.assertFalse(DestinoTuristico.objects.filter(id=d.id).exists())

    def test_crud_plato(self):
        self.entrar('Administrador')
        datos = {'nombre': 'Charquicán', 'region': 'Centro', 'descripcion': 'Guiso',
                 'imagen': 'c.jpg', 'dificultad': 'Media', 'tiempo_preparacion': 50,
                 'porciones': 4, 'precio_referencia': 5000, 'ingredientes': 'Zapallo, Papa'}
        self.client.post(reverse('gastronomia_plato_crear'), datos)
        p = PlatoTipico.objects.get(nombre='Charquicán')
        r = self.client.get(reverse('gastronomia_plato_lista'), {'q': 'Charqui'})
        self.assertContains(r, 'Charquicán')
        datos['porciones'] = 6
        self.client.post(reverse('gastronomia_plato_editar', args=[p.id]), datos)
        p.refresh_from_db()
        self.assertEqual(p.porciones, 6)
        self.client.post(reverse('gastronomia_plato_eliminar', args=[p.id]))
        self.assertFalse(PlatoTipico.objects.filter(id=p.id).exists())

    def test_validacion_formulario(self):
        self.entrar('Administrador')
        r = self.client.post(reverse('gastronomia_plato_crear'), {'nombre': ''})
        self.assertEqual(r.status_code, 200)
        self.assertFalse(PlatoTipico.objects.filter(nombre='').exists())


class TransaccionReservaTests(SistemaTestBase):
    def test_crear_reserva_relaciona_entidades(self):
        self.entrar('Administrativo')
        manana = (date.today() + timedelta(days=1)).isoformat()
        r = self.client.post(reverse('turismo_reserva_crear'), {
            'destino': self.destino.id, 'plato': self.plato.id, 'fecha_reserva': manana,
            'num_personas': 2, 'estado': 'Pendiente', 'observaciones': 'Vegetariano'})
        self.assertRedirects(r, reverse('turismo_reserva_lista'))
        reserva = ReservaTuristica.objects.get()
        self.assertEqual(reserva.usuario, self.usuarios['Administrativo'])
        self.assertEqual(reserva.costo_total(), (30000 + 4000) * 2)

    def test_validaciones_reserva(self):
        self.entrar('Administrativo')
        ayer = (date.today() - timedelta(days=1)).isoformat()
        r = self.client.post(reverse('turismo_reserva_crear'), {
            'destino': self.destino.id, 'fecha_reserva': ayer,
            'num_personas': 0, 'estado': 'Pendiente'})
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, 'no puede ser anterior a hoy')
        self.assertEqual(ReservaTuristica.objects.count(), 0)


class RecuperacionContrasenaTests(SistemaTestBase):
    def test_flujo_completo(self):
        # 1. Solicitar recuperación
        r = self.client.post(reverse('password_reset'), {'email': 'ana@test.cl'})
        self.assertRedirects(r, reverse('password_reset_done'))
        # 2-3. Correo enviado con enlace y token
        self.assertEqual(len(mail.outbox), 1)
        enlace = re.search(r'http://testserver(/password-reset/\S+/\S+/)', mail.outbox[0].body).group(1)
        # 4. Validar token (Django redirige a una URL segura de "set-password")
        r = self.client.get(enlace, follow=True)
        self.assertTrue(r.context['validlink'])
        url_form = r.redirect_chain[-1][0]
        # 5. Establecer nueva contraseña
        nueva = 'NuevaClave2026!'
        r = self.client.post(url_form, {'new_password1': nueva, 'new_password2': nueva})
        # 6. Confirmar cambio exitoso
        self.assertRedirects(r, reverse('password_reset_complete'))
        # Acceso con la nueva contraseña
        self.assertTrue(self.client.login(username='ana', password=nueva))

    def test_token_invalido(self):
        r = self.client.get('/password-reset/MQ/token-falso/')
        self.assertFalse(r.context['validlink'])
