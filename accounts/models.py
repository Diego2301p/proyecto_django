"""
accounts/models.py - Modelos de la app de cuentas.

Se utiliza el modelo User de Django (django.contrib.auth.models.User)
y el sistema de Grupos (Group) para manejar los perfiles:
- Administrador: acceso total al sistema.
- Supervisor: permisos intermedios.
- Administrativo: permisos mínimos.

No se requieren modelos adicionales en esta app.
"""
from django.db import models

