"""
app_gastronomia/views.py - Vistas de la aplicación de platos típicos chilenos.

Contiene las vistas funcionales que leen datos desde platos.json,
los procesan usando funciones auxiliares y los envían a las plantillas.
La temática es claramente distinta a app_turismo (gastronomía vs. turismo).

Librería externa utilizada: humanize
Se usa para formatear precios y tiempos de preparación de forma
legible para el usuario.
"""

import json
import os
from django.shortcuts import render
from django.conf import settings
# humanize: librería externa para formateo legible de números
import humanize


# ============================================================
# FUNCIONES AUXILIARES (Requisito 2.2)
# ============================================================

def cargar_platos():
    """
    Lee y retorna la lista de platos típicos desde el archivo JSON.
    Maneja errores con try/except (Requisito 8).

    Returns:
        list: Lista de diccionarios con los datos de platos, o lista
              vacía si ocurre un error.
    """
    ruta_json = os.path.join(
        settings.BASE_DIR, 'app_gastronomia', 'data', 'platos.json'
    )
    try:
        with open(ruta_json, 'r', encoding='utf-8') as archivo:
            datos = json.load(archivo)
        return datos
    except FileNotFoundError:
        print(f"[ERROR] No se encontró el archivo: {ruta_json}")
        return []
    except json.JSONDecodeError:
        print(f"[ERROR] El archivo {ruta_json} no tiene formato JSON válido")
        return []


def filtrar_por_dificultad(platos, dificultad):
    """
    Filtra platos por nivel de dificultad.
    Usa bucle for y comparación de strings (Requisitos 2.1, 2.2).

    Args:
        platos (list): Lista completa de platos.
        dificultad (str): Nivel de dificultad ("Baja", "Media", "Alta").

    Returns:
        list: Sublista de platos con la dificultad indicada.
    """
    resultado = []
    for plato in platos:
        if plato.get('dificultad', '').lower() == dificultad.lower():
            resultado.append(plato)
    return resultado


def obtener_niveles_dificultad(platos):
    """
    Extrae los niveles de dificultad únicos de la lista de platos.

    Args:
        platos (list): Lista completa de platos.

    Returns:
        list: Lista de niveles de dificultad únicos.
    """
    niveles = set()
    for plato in platos:
        nivel = plato.get('dificultad', '')
        if nivel:  # bool check: solo si no está vacío
            niveles.add(nivel)
    # Ordenar por dificultad lógica (no alfabética)
    orden = {'Baja': 1, 'Media': 2, 'Alta': 3}
    return sorted(list(niveles), key=lambda x: orden.get(x, 99))


def calcular_estadisticas_gastronomia(platos):
    """
    Calcula estadísticas sobre los platos típicos.
    Demuestra operadores aritméticos, lógicos y de comparación (Req 2.1).

    Args:
        platos (list): Lista completa de platos.

    Returns:
        dict: Diccionario con estadísticas calculadas.
    """
    total_platos = len(platos)  # int
    if total_platos == 0:
        return {
            'total': 0,
            'tiempo_promedio': 0,
            'platos_vegetarianos': 0,
            'ingredientes_totales': 0,
            'precio_promedio': '0',
        }

    tiempos = []          # list de int
    vegetarianos = 0      # int: contador
    total_ingredientes = 0  # int: acumulador
    precios = []          # list de int

    # Bucle for para recorrer todos los platos (Requisito 2.2)
    for plato in platos:
        tiempo = plato.get('tiempo_preparacion', 0)  # int
        es_vegetariano = plato.get('es_vegetariano', False)  # bool
        ingredientes = plato.get('ingredientes', [])  # list
        precio = plato.get('precio_referencia', 0)  # int

        tiempos.append(tiempo)
        precios.append(precio)

        # Operador lógico: si es vegetariano Y tiene ingredientes
        if es_vegetariano and len(ingredientes) > 0:
            vegetarianos += 1  # Operador aritmético
        elif es_vegetariano:
            vegetarianos += 1

        # Acumular total de ingredientes (operador aritmético: +=)
        total_ingredientes += len(ingredientes)

    # Cálculos con operadores aritméticos
    tiempo_promedio = sum(tiempos) // total_platos  # División entera
    precio_promedio = sum(precios) / total_platos   # División flotante

    return {
        'total': total_platos,
        'tiempo_promedio': tiempo_promedio,
        'platos_vegetarianos': vegetarianos,
        'ingredientes_totales': total_ingredientes,
        'precio_promedio': humanize.intcomma(int(precio_promedio)),
        'ingredientes_promedio': round(total_ingredientes / total_platos, 1),
    }


def formatear_tiempo(minutos):
    """
    Convierte minutos a formato de horas y minutos legible.
    Demuestra operadores aritméticos (división entera y módulo).

    Args:
        minutos (int): Tiempo en minutos.

    Returns:
        str: Tiempo formateado (ej: "1 h 30 min" o "45 min").
    """
    if minutos >= 60:
        horas = minutos // 60    # Operador: división entera
        mins = minutos % 60      # Operador: módulo (resto)
        if mins > 0:
            return f"{horas} h {mins} min"
        else:
            return f"{horas} h"
    else:
        return f"{minutos} min"


def procesar_platos_para_vista(platos):
    """
    Enriquece la lista de platos con datos formateados para la vista.
    Agrega precio formateado, tiempo legible y conteo de ingredientes.

    Args:
        platos (list): Lista de platos sin procesar.

    Returns:
        list: Lista de platos con campos adicionales formateados.
    """
    platos_procesados = []
    for plato in platos:
        plato_copia = plato.copy()  # No mutar el original
        # Formatear precio con humanize
        plato_copia['precio_formateado'] = humanize.intcomma(
            plato.get('precio_referencia', 0)
        )
        # Formatear tiempo de preparación
        plato_copia['tiempo_formateado'] = formatear_tiempo(
            plato.get('tiempo_preparacion', 0)
        )
        # Contar ingredientes
        plato_copia['num_ingredientes'] = len(
            plato.get('ingredientes', [])
        )
        platos_procesados.append(plato_copia)
    return platos_procesados


# ============================================================
# VISTAS FUNCIONALES (Requisitos 1.4 y 6)
# ============================================================

def inicio_gastronomia(request):
    """
    Vista de presentación de la sección de gastronomía chilena.
    Muestra un resumen de platos y estadísticas.

    Demuestra:
    - Lectura de JSON con cargar_platos()
    - Procesamiento con funciones auxiliares
    - Contexto enviado a la plantilla
    - Estructuras if/elif/else para mensajes dinámicos
    """
    platos = cargar_platos()
    estadisticas = calcular_estadisticas_gastronomia(platos)
    platos_procesados = procesar_platos_para_vista(platos)

    # Estructura de control if/elif/else (Requisito 2.1)
    total = estadisticas['total']
    if total >= 6:
        mensaje = "¡Explora nuestra completa colección de recetas tradicionales!"
    elif total >= 3:
        mensaje = "Descubre algunos de los platos más emblemáticos de Chile."
    else:
        mensaje = "Pronto agregaremos más recetas chilenas."

    # Separar platos rápidos (< 60 min) y elaborados (>= 60 min)
    platos_rapidos = []
    platos_elaborados = []
    for plato in platos_procesados:
        tiempo = plato.get('tiempo_preparacion', 0)
        # Operador de comparación: menor que
        if tiempo < 60:
            platos_rapidos.append(plato)
        else:
            platos_elaborados.append(plato)

    contexto = {
        'titulo': 'Gastronomía Chilena',
        'mensaje': mensaje,
        'platos': platos_procesados,
        'estadisticas': estadisticas,
        'platos_rapidos': len(platos_rapidos),
        'platos_elaborados': len(platos_elaborados),
    }

    return render(request, 'app_gastronomia/inicio_gastronomia.html', contexto)


def platos_tipicos(request):
    """
    Vista que muestra el listado completo de platos típicos.
    Permite filtrar por dificultad mediante parámetro GET.

    Demuestra:
    - Lectura de parámetros GET del request
    - Filtrado condicional con función auxiliar
    - Procesamiento con bucles antes de enviar al template
    """
    todos_los_platos = cargar_platos()

    # Leer parámetro de filtro desde la URL (ej: ?dificultad=Baja)
    filtro_dificultad = request.GET.get('dificultad', '')  # str

    # Estructura de control: aplicar filtro si existe
    if filtro_dificultad and filtro_dificultad != 'Todas':
        platos_mostrados = filtrar_por_dificultad(
            todos_los_platos, filtro_dificultad
        )
        titulo_pagina = f'Platos - Dificultad {filtro_dificultad}'
    else:
        platos_mostrados = todos_los_platos
        titulo_pagina = 'Todos los Platos Típicos'

    # Procesar platos para la vista (formatear precios, tiempos)
    platos_procesados = procesar_platos_para_vista(platos_mostrados)

    # Obtener niveles de dificultad para el filtro
    niveles = obtener_niveles_dificultad(todos_los_platos)

    # Comparación: verificar si hay resultados (bool)
    hay_resultados = len(platos_procesados) > 0

    contexto = {
        'titulo': titulo_pagina,
        'platos': platos_procesados,
        'niveles_dificultad': niveles,
        'dificultad_actual': filtro_dificultad,
        'hay_resultados': hay_resultados,
        'total_mostrados': len(platos_procesados),
        'total_general': len(todos_los_platos),
    }

    return render(request, 'app_gastronomia/platos.html', contexto)


def detalle_plato(request, plato_id):
    """
    Vista de detalle de un plato típico específico.
    Recibe el ID del plato como parámetro de la URL.

    Demuestra:
    - Búsqueda por ID con bucle while
    - Manejo del caso "no encontrado"
    """
    platos = cargar_platos()

    # Búsqueda con while (Requisito 2.2)
    plato_encontrado = None
    idx = 0  # int: índice

    while idx < len(platos):
        if platos[idx].get('id') == plato_id:
            plato_encontrado = platos[idx].copy()
            break
        idx += 1

    # Procesar el plato encontrado
    if plato_encontrado is not None:
        plato_encontrado['precio_formateado'] = humanize.intcomma(
            plato_encontrado.get('precio_referencia', 0)
        )
        plato_encontrado['tiempo_formateado'] = formatear_tiempo(
            plato_encontrado.get('tiempo_preparacion', 0)
        )
        plato_encontrado['num_ingredientes'] = len(
            plato_encontrado.get('ingredientes', [])
        )
        titulo = plato_encontrado.get('nombre', 'Plato')
        encontrado = True
    else:
        titulo = 'Plato no encontrado'
        encontrado = False

    contexto = {
        'titulo': titulo,
        'plato': plato_encontrado,
        'encontrado': encontrado,
    }

    return render(request, 'app_gastronomia/detalle_plato.html', contexto)
