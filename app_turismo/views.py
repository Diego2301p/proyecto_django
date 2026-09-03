"""
app_turismo/views.py - Vistas de la aplicación de destinos turísticos de Chile.

Contiene las vistas funcionales que leen datos desde destinos.json,
los procesan usando funciones auxiliares y los envían a las plantillas
mediante el diccionario de contexto.

Librería externa utilizada: humanize
Se usa para formatear números (precios) de forma legible para humanos,
por ejemplo: 45000 → "45.000" (formato chileno). Esto mejora la
presentación de datos numéricos en la interfaz.
"""

import json
import os
from django.shortcuts import render
from django.conf import settings
# humanize: librería externa para formatear números y fechas de forma
# legible para humanos (ej: intcomma convierte 45000 → "45,000")
import humanize


# ============================================================
# FUNCIONES AUXILIARES (Requisito 2.2)
# ============================================================

def cargar_destinos():
    """
    Lee y retorna la lista de destinos turísticos desde el archivo JSON.
    Usa try/except para manejar errores si el archivo no existe o está
    mal formado (Requisito 8: manejo de errores).

    Returns:
        list: Lista de diccionarios con los datos de destinos, o lista
              vacía si ocurre un error.
    """
    # Construimos la ruta absoluta al archivo JSON usando os.path
    ruta_json = os.path.join(
        settings.BASE_DIR, 'app_turismo', 'data', 'destinos.json'
    )
    try:
        # Abrimos el archivo con codificación UTF-8 para soportar
        # caracteres especiales (tildes, eñes)
        with open(ruta_json, 'r', encoding='utf-8') as archivo:
            datos = json.load(archivo)  # Deserializa el JSON a Python
        return datos
    except FileNotFoundError:
        # El archivo JSON no existe en la ruta esperada
        print(f"[ERROR] No se encontró el archivo: {ruta_json}")
        return []
    except json.JSONDecodeError:
        # El archivo existe pero tiene formato JSON inválido
        print(f"[ERROR] El archivo {ruta_json} no tiene formato JSON válido")
        return []


def filtrar_destinos_por_categoria(destinos, categoria):
    """
    Filtra la lista de destinos por una categoría específica.
    Usa un bucle for para recorrer la lista y comparación de strings
    (Requisitos 2.1 y 2.2).

    Args:
        destinos (list): Lista completa de destinos.
        categoria (str): Categoría a filtrar (ej: "Naturaleza", "Cultura").

    Returns:
        list: Sublista de destinos que coinciden con la categoría.
    """
    destinos_filtrados = []  # Lista vacía para acumular resultados
    for destino in destinos:
        # Comparación case-insensitive para mayor flexibilidad
        if destino.get('categoria', '').lower() == categoria.lower():
            destinos_filtrados.append(destino)
    return destinos_filtrados


def obtener_categorias_unicas(destinos):
    """
    Extrae las categorías únicas de la lista de destinos.
    Útil para generar filtros dinámicos en la interfaz.

    Args:
        destinos (list): Lista completa de destinos.

    Returns:
        list: Lista ordenada de categorías únicas.
    """
    categorias = set()  # Usamos set para evitar duplicados
    for destino in destinos:
        categoria = destino.get('categoria', '')
        if categoria:  # Solo agregamos si no está vacío (bool check)
            categorias.add(categoria)
    return sorted(list(categorias))  # Retornamos lista ordenada


def calcular_estadisticas(destinos):
    """
    Calcula estadísticas generales sobre los destinos turísticos.
    Demuestra uso de operadores aritméticos, variables numéricas
    y estructuras de control (Requisito 2.1).

    Args:
        destinos (list): Lista completa de destinos.

    Returns:
        dict: Diccionario con estadísticas calculadas.
    """
    total_destinos = len(destinos)  # int: cantidad total
    if total_destinos == 0:
        return {
            'total': 0,
            'precio_promedio': 0,
            'precio_minimo': 0,
            'precio_maximo': 0,
            'puntuacion_promedio': 0.0,
            'destinos_destacados': 0,
        }

    # Variables numéricas (int y float) para cálculos
    precios = []     # list de int
    puntuaciones = []  # list de float
    destacados = 0   # int: contador

    for destino in destinos:
        precio = destino.get('precio_estimado', 0)  # int
        puntuacion = destino.get('puntuacion', 0.0)  # float
        es_destacado = destino.get('destacado', False)  # bool

        precios.append(precio)
        puntuaciones.append(puntuacion)

        # Operador lógico: si es destacado, incrementamos el contador
        if es_destacado:
            destacados += 1  # Operador aritmético: suma

    # Operadores aritméticos: suma, división, min, max
    precio_promedio = sum(precios) / total_destinos  # float: división
    puntuacion_promedio = sum(puntuaciones) / total_destinos

    return {
        'total': total_destinos,
        'precio_promedio': formatear_precio(int(precio_promedio)),
        'precio_minimo': formatear_precio(min(precios)),
        'precio_maximo': formatear_precio(max(precios)),
        'puntuacion_promedio': round(puntuacion_promedio, 1),
        'destinos_destacados': destacados,
    }


def formatear_precio(precio):
    """
    Formatea un precio entero a formato legible con separador de miles.
    Usa la librería externa 'humanize' (Requisito 2.3).

    Args:
        precio (int): Precio en pesos chilenos.

    Returns:
        str: Precio formateado (ej: "45,000").
    """
    # humanize.intcomma agrega separadores de miles
    return humanize.intcomma(precio)


def obtener_destinos_destacados(destinos):
    """
    Filtra y retorna solo los destinos marcados como destacados.
    Demuestra uso de bool y operadores de comparación.

    Args:
        destinos (list): Lista completa de destinos.

    Returns:
        list: Destinos donde 'destacado' es True.
    """
    destacados = []
    for destino in destinos:
        # Operador de comparación: verificamos si es True (bool)
        if destino.get('destacado', False) == True:
            # Agregamos el precio formateado al destino
            destino_copia = destino.copy()  # No mutar el original
            destino_copia['precio_formateado'] = formatear_precio(
                destino.get('precio_estimado', 0)
            )
            destacados.append(destino_copia)
    return destacados


# ============================================================
# VISTAS FUNCIONALES (Requisitos 1.4 y 6)
# ============================================================

def inicio(request):
    """
    Vista de inicio/presentación general del sitio.
    Muestra los destinos destacados y estadísticas generales.
    Es la página principal a la que redirige la ruta '/'.

    Demuestra:
    - Lectura de JSON (cargar_destinos)
    - Procesamiento de datos (funciones auxiliares)
    - Envío de contexto a la plantilla con render()
    - Uso de if/elif/else para determinar mensajes dinámicos
    """
    # Leer datos desde el archivo JSON
    destinos = cargar_destinos()

    # Procesar datos usando funciones auxiliares
    estadisticas = calcular_estadisticas(destinos)
    destacados = obtener_destinos_destacados(destinos)
    categorias = obtener_categorias_unicas(destinos)

    # Estructura de control if/elif/else para mensaje dinámico
    total = estadisticas['total']  # int
    if total >= 6:
        mensaje_bienvenida = "¡Tenemos una amplia selección de destinos para ti!"
    elif total >= 3:
        mensaje_bienvenida = "Descubre nuestros destinos seleccionados."
    else:
        mensaje_bienvenida = "Pronto agregaremos más destinos."

    # Diccionario de contexto que se envía a la plantilla
    contexto = {
        'titulo': 'Chile Descubre - Inicio',
        'mensaje_bienvenida': mensaje_bienvenida,
        'destacados': destacados,
        'estadisticas': estadisticas,
        'categorias': categorias,
        'total_destinos': total,
    }

    # render() combina la plantilla con el contexto y retorna HttpResponse
    return render(request, 'app_turismo/inicio.html', contexto)


def destinos(request):
    """
    Vista que muestra el listado completo de destinos turísticos.
    Permite filtrar por categoría mediante parámetro GET.

    Demuestra:
    - Lectura de parámetros GET del request
    - Filtrado condicional de datos
    - Bucles y procesamiento antes de enviar a la plantilla
    """
    # Leer todos los destinos desde el JSON
    todos_los_destinos = cargar_destinos()

    # Obtener parámetro de filtro desde la URL (ej: ?categoria=Naturaleza)
    categoria_filtro = request.GET.get('categoria', '')  # str, vacío si no viene

    # Estructura de control: si hay filtro, aplicarlo
    if categoria_filtro and categoria_filtro != 'Todas':
        destinos_mostrados = filtrar_destinos_por_categoria(
            todos_los_destinos, categoria_filtro
        )
        titulo_pagina = f'Destinos - {categoria_filtro}'
    else:
        destinos_mostrados = todos_los_destinos
        titulo_pagina = 'Todos los Destinos Turísticos'

    # Procesar cada destino para agregar datos formateados
    # Bucle for para recorrer y enriquecer la lista (Requisito 2.2)
    destinos_procesados = []
    for destino in destinos_mostrados:
        destino_copia = destino.copy()
        destino_copia['precio_formateado'] = formatear_precio(
            destino.get('precio_estimado', 0)
        )
        # Contar actividades disponibles (len sobre lista)
        actividades = destino.get('actividades', [])
        destino_copia['num_actividades'] = len(actividades)
        destinos_procesados.append(destino_copia)

    # Obtener categorías para el filtro
    categorias = obtener_categorias_unicas(todos_los_destinos)

    # Comparación: verificar si hay resultados
    hay_resultados = len(destinos_procesados) > 0  # bool

    contexto = {
        'titulo': titulo_pagina,
        'destinos': destinos_procesados,
        'categorias': categorias,
        'categoria_actual': categoria_filtro,
        'hay_resultados': hay_resultados,
        'total_mostrados': len(destinos_procesados),
        'total_general': len(todos_los_destinos),
    }

    return render(request, 'app_turismo/destinos.html', contexto)


def detalle_destino(request, destino_id):
    """
    Vista de detalle de un destino turístico específico.
    Recibe el ID del destino como parámetro de la URL.

    Demuestra:
    - Búsqueda por ID en una lista de diccionarios
    - Manejo de caso "no encontrado"
    - Uso de while para buscar en la lista
    """
    destinos = cargar_destinos()

    # Búsqueda del destino por ID usando while (Requisito 2.2)
    destino_encontrado = None
    indice = 0  # int: índice para recorrer la lista

    while indice < len(destinos):
        if destinos[indice].get('id') == destino_id:
            destino_encontrado = destinos[indice].copy()
            break  # Salir del while al encontrar el destino
        indice += 1  # Operador aritmético: incremento

    # Estructura de control: verificar si se encontró
    if destino_encontrado is not None:
        # Enriquecer datos del destino encontrado
        destino_encontrado['precio_formateado'] = formatear_precio(
            destino_encontrado.get('precio_estimado', 0)
        )
        titulo = destino_encontrado.get('nombre', 'Destino')
        encontrado = True
    else:
        titulo = 'Destino no encontrado'
        encontrado = False

    contexto = {
        'titulo': titulo,
        'destino': destino_encontrado,
        'encontrado': encontrado,
    }

    return render(request, 'app_turismo/detalle_destino.html', contexto)
