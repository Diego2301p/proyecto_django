"""
Management command: cargar_datos_iniciales

Carga los datos iniciales desde los archivos JSON (destinos.json y platos.json)
hacia la base de datos MySQL. Este comando se ejecuta una sola vez después de
correr las migraciones para poblar la base de datos.

Uso:
    python manage.py cargar_datos_iniciales
"""

import json
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from app_turismo.models import DestinoTuristico
from app_gastronomia.models import PlatoTipico


class Command(BaseCommand):
    help = 'Carga los datos iniciales desde los archivos JSON hacia la base de datos MySQL.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE('=== Cargando datos iniciales ==='))
        self.stdout.write('')

        # Cargar destinos turísticos
        self.cargar_destinos()

        # Cargar platos típicos
        self.cargar_platos()

        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('=== Datos iniciales cargados exitosamente ==='))

    def cargar_destinos(self):
        """Carga los destinos turísticos desde destinos.json."""
        ruta_json = os.path.join(
            settings.BASE_DIR, 'app_turismo', 'data', 'destinos.json'
        )

        try:
            with open(ruta_json, 'r', encoding='utf-8') as archivo:
                datos = json.load(archivo)
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f'No se encontró: {ruta_json}'))
            return
        except json.JSONDecodeError:
            self.stdout.write(self.style.ERROR(f'JSON inválido: {ruta_json}'))
            return

        # Verificar si ya hay datos
        if DestinoTuristico.objects.exists():
            self.stdout.write(self.style.WARNING(
                f'Ya existen {DestinoTuristico.objects.count()} destinos en la BD. '
                'Se omite la carga para evitar duplicados.'
            ))
            return

        contador = 0
        for item in datos:
            # Convertir lista de actividades a string separado por comas
            actividades = item.get('actividades', [])
            actividades_str = ', '.join(actividades) if isinstance(actividades, list) else str(actividades)

            DestinoTuristico.objects.create(
                nombre=item.get('nombre', ''),
                region=item.get('region', ''),
                descripcion=item.get('descripcion', ''),
                imagen=item.get('imagen', ''),
                categoria=item.get('categoria', ''),
                precio_estimado=item.get('precio_estimado', 0),
                puntuacion=item.get('puntuacion', 0.0),
                destacado=item.get('destacado', False),
                actividades=actividades_str,
            )
            contador += 1
            self.stdout.write(f'  ✓ Destino creado: {item.get("nombre")}')

        self.stdout.write(self.style.SUCCESS(
            f'Se cargaron {contador} destinos turísticos.'
        ))

    def cargar_platos(self):
        """Carga los platos típicos desde platos.json."""
        ruta_json = os.path.join(
            settings.BASE_DIR, 'app_gastronomia', 'data', 'platos.json'
        )

        try:
            with open(ruta_json, 'r', encoding='utf-8') as archivo:
                datos = json.load(archivo)
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f'No se encontró: {ruta_json}'))
            return
        except json.JSONDecodeError:
            self.stdout.write(self.style.ERROR(f'JSON inválido: {ruta_json}'))
            return

        # Verificar si ya hay datos
        if PlatoTipico.objects.exists():
            self.stdout.write(self.style.WARNING(
                f'Ya existen {PlatoTipico.objects.count()} platos en la BD. '
                'Se omite la carga para evitar duplicados.'
            ))
            return

        contador = 0
        for item in datos:
            # Convertir lista de ingredientes a string separado por comas
            ingredientes = item.get('ingredientes', [])
            ingredientes_str = ', '.join(ingredientes) if isinstance(ingredientes, list) else str(ingredientes)

            PlatoTipico.objects.create(
                nombre=item.get('nombre', ''),
                region=item.get('region', ''),
                descripcion=item.get('descripcion', ''),
                imagen=item.get('imagen', ''),
                dificultad=item.get('dificultad', 'Media'),
                tiempo_preparacion=item.get('tiempo_preparacion', 0),
                porciones=item.get('porciones', 1),
                es_vegetariano=item.get('es_vegetariano', False),
                precio_referencia=item.get('precio_referencia', 0),
                ingredientes=ingredientes_str,
            )
            contador += 1
            self.stdout.write(f'  ✓ Plato creado: {item.get("nombre")}')

        self.stdout.write(self.style.SUCCESS(
            f'Se cargaron {contador} platos típicos.'
        ))
