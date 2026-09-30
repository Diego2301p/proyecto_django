# 🇨🇱 Chile Descubre

Portal informativo sobre destinos turísticos y gastronomía típica de Chile.  
Desarrollado con **Django 6.1** + **MySQL** + desplegado en **AWS EC2**.

---

## 📋 Descripción del Proyecto

**Chile Descubre** es una aplicación web académica que permite explorar:
- **Destinos turísticos** de Chile (Torres del Paine, San Pedro de Atacama, Valparaíso, etc.)
- **Platos típicos** de la gastronomía chilena (Empanadas, Pastel de Choclo, Cazuela, etc.)

La información se almacena en una base de datos **MySQL** y se administra mediante **Django Admin**.

---

## 🏗️ Arquitectura del Proyecto

```
proyecto_django/
├── app_turismo/          # App de destinos turísticos
│   ├── models.py         # Modelo: DestinoTuristico
│   ├── views.py          # Vistas con Django ORM
│   ├── urls.py           # Rutas /turismo/
│   ├── admin.py          # Registro en Django Admin
│   ├── data/             # JSON con datos iniciales
│   └── templates/        # Plantillas HTML
├── app_gastronomia/      # App de platos típicos
│   ├── models.py         # Modelo: PlatoTipico
│   ├── views.py          # Vistas con Django ORM
│   ├── urls.py           # Rutas /gastronomia/
│   ├── admin.py          # Registro en Django Admin
│   ├── data/             # JSON con datos iniciales
│   └── templates/        # Plantillas HTML
├── config/               # Configuración Django
│   ├── settings.py       # Ajustes (MySQL, Admin, etc.)
│   └── urls.py           # URLs raíz
├── templates/            # Plantillas globales (base.html)
├── static/               # CSS, JS, Imágenes (Bootstrap local)
├── requirements.txt      # Dependencias Python
└── .env                  # Variables de entorno (no en git)
```

---

## 🗄️ Base de Datos

**Motor**: MySQL  
**Base de datos**: `chile_descubre`

### Modelos implementados:

| Modelo | App | Descripción |
|--------|-----|-------------|
| `DestinoTuristico` | app_turismo | Destinos turísticos de Chile |
| `PlatoTipico` | app_gastronomia | Platos típicos de la gastronomía chilena |

---

## 🚀 Despliegue

- **Plataforma**: Amazon AWS EC2
- **Sistema operativo**: Ubuntu Server 24.04 LTS
- **IP del servidor**: 100.56.39.123
- **Puerto**: 8000
- **Control de versiones**: Git + GitHub

---

## ⚙️ Instalación local

### 1. Clonar el repositorio
```bash
git clone https://github.com/Diego2301p/proyecto_django.git
cd proyecto_django
```

### 2. Crear entorno virtual
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno
Crear archivo `.env` en la raíz del proyecto:
```
DB_ENGINE=django.db.backends.mysql
DB_NAME=chile_descubre
DB_USER=user_chile
DB_PASSWORD=TU_PASSWORD_SEGURA
DB_HOST=localhost
DB_PORT=3306
```

### 5. Ejecutar migraciones y cargar datos
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py cargar_datos_iniciales
```

### 6. Correr el servidor
```bash
python manage.py runserver
```

Visita: http://localhost:8000

---

## 🛠️ Tecnologías

| Tecnología | Versión |
|-----------|---------|
| Python | 3.12 |
| Django | 6.1.1 |
| MySQL | 8.x |
| Bootstrap | 5 (local) |
| humanize | 4.16.0 |
| python-dotenv | 1.1.0 |
| mysqlclient | 2.2.7 |

---

## 📁 Archivos importantes

- `.gitignore` — excluye `venv/`, `.env`, `__pycache__/`, `staticfiles/`
- `requirements.txt` — dependencias del proyecto
- `manage.py` — punto de entrada de Django
- `.env` — variables de entorno (**NO incluido en el repositorio**)

---

## 👤 Autor

**Diego** — Proyecto académico Back End | INACAP La Serena | Primavera 2026
