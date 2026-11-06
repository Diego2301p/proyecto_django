# 🇨🇱 Chile Descubre

Aplicación web sobre destinos turísticos y gastronomía típica de Chile, con gestión de usuarios por roles, mantenedores CRUD y sistema de reservas.
Desarrollada con **Django 6.1** + **MySQL** + **Bootstrap 5** y desplegada en **AWS EC2**.

---

## 📋 Descripción del Proyecto

**Chile Descubre** permite consultar y administrar:
- **Destinos turísticos** de Chile (Torres del Paine, San Pedro de Atacama, Valparaíso, etc.)
- **Platos típicos** de la gastronomía chilena (Empanadas, Pastel de Choclo, Cazuela, etc.)
- **Reservas turísticas** asociadas a un destino y opcionalmente a un plato típico.
- **Usuarios y perfiles** (`Administrador`, `Supervisor` y `Administrativo`), cada uno con su propio dashboard y nivel de permisos, además de recuperación de contraseña por correo electrónico.

---

## 🏗️ Estructura del Proyecto

```
proyecto_django/
├── accounts/             # Autenticación, perfiles, dashboards y usuarios
│   ├── decorators.py     # Control de acceso por grupo
│   ├── forms.py          # Formularios de login y usuarios
│   ├── views.py          # Vistas de sesión, paneles y CRUD usuarios
│   ├── urls.py           # Rutas /accounts/
│   └── templates/        # Plantillas de cuentas y recuperación de clave
├── app_turismo/          # Destinos turísticos y reservas
│   ├── models.py         # DestinoTuristico y ReservaTuristica
│   ├── forms.py          # Formularios de destinos y reservas
│   ├── views.py          # Vistas públicas y mantenedores
│   ├── urls.py           # Rutas /turismo/
│   ├── data/             # JSON con datos iniciales
│   └── templates/        # Plantillas HTML
├── app_gastronomia/      # Platos típicos chilenos
│   ├── models.py         # PlatoTipico
│   ├── forms.py          # Formulario de platos
│   ├── views.py          # Vistas públicas y mantenedor
│   ├── urls.py           # Rutas /gastronomia/
│   ├── data/             # JSON con datos iniciales
│   └── templates/        # Plantillas HTML
├── config/               # Configuración general de Django
│   ├── settings.py       # Base de datos, correo SMTP y sesiones
│   └── urls.py           # Rutas principales
├── templates/            # Plantillas globales (base.html)
├── static/               # CSS, JS e imágenes (Bootstrap local)
├── requirements.txt      # Dependencias Python
└── .env                  # Variables de entorno (no incluido en git)
```

---

## 🗄️ Base de Datos

**Motor**: MySQL  
**Base de datos**: `chile_descubre`

| Modelo | App | Descripción |
|--------|-----|-------------|
| `DestinoTuristico` | app_turismo | Destinos turísticos de Chile |
| `PlatoTipico` | app_gastronomia | Platos típicos de la gastronomía chilena |
| `ReservaTuristica` | app_turismo | Reservas asociadas a usuario, destino y plato |
| `User` / `Group` | django.contrib.auth | Cuentas de usuario y perfiles de acceso |

---

## 🚀 Despliegue

- **Plataforma**: Amazon AWS EC2
- **Sistema operativo**: Ubuntu Server LTS
- **IP del servidor**: 100.56.39.123
- **Puerto**: 8000
- **Control de versiones**: Git + GitHub

---

## ⚙️ Instalación

### 1. Clonar el repositorio y activar entorno virtual
```bash
git clone https://github.com/Diego2301p/proyecto_django.git
cd proyecto_django
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

### 2. Configurar variables de entorno (`.env`)
```env
DB_ENGINE=django.db.backends.mysql
DB_NAME=chile_descubre
DB_USER=user_chile
DB_PASSWORD=TU_PASSWORD_SEGURA
DB_HOST=localhost
DB_PORT=3306

EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=tu_correo@gmail.com
EMAIL_HOST_PASSWORD=tu_clave_de_aplicacion
```

### 3. Ejecutar migraciones, datos iniciales y roles
```bash
python manage.py migrate
python manage.py cargar_datos_iniciales
python manage.py crear_roles --usuarios-demo
python manage.py runserver
```

### Perfiles de prueba (`crear_roles --usuarios-demo`)

| Usuario | Contraseña | Perfil |
|---------|------------|--------|
| `admin` | `Dark2301$` | Administrador |
| `supervisor` | `Dark2301$` | Supervisor |
| `administrativo` | `Dark2301$` | Administrativo |

---

## 🛠️ Tecnologías

| Tecnología | Versión |
|-----------|---------|
| Python | 3.12+ |
| Django | 6.1.1 |
| MySQL | 8.x |
| Bootstrap | 5 (local) |
| humanize | 4.16.0 |
| python-dotenv | 1.1.0 |
| mysqlclient | 2.2.7 |

---

## 👤 Autor

**Diego** - Proyecto académico Back End | INACAP La Serena | Primavera 2026
