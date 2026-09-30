"""
app_gastronomia/models.py - Modelos ORM de la aplicación de gastronomía.

Define el modelo PlatoTipico que representa un plato típico chileno
en la base de datos MySQL. Reemplaza la lectura de datos desde
archivos JSON por el ORM de Django.
"""

from django.db import models


class PlatoTipico(models.Model):
    """
    Modelo que representa un plato típico chileno.

    Campos:
        nombre (str): Nombre del plato (ej: "Empanada de Pino").
        region (str): Región o zona de Chile donde es típico.
        descripcion (str): Descripción detallada del plato.
        imagen (str): Nombre del archivo de imagen en static/img/.
        dificultad (str): Nivel de dificultad (Baja, Media, Alta).
        tiempo_preparacion (int): Tiempo de preparación en minutos.
        porciones (int): Cantidad de porciones que rinde.
        es_vegetariano (bool): Si el plato es vegetariano.
        precio_referencia (int): Precio referencial en pesos chilenos.
        ingredientes (str): Ingredientes separados por coma.
    """
    nombre = models.CharField(max_length=200, verbose_name='Nombre')
    region = models.CharField(max_length=200, verbose_name='Región')
    descripcion = models.TextField(verbose_name='Descripción')
    imagen = models.CharField(max_length=200, verbose_name='Imagen')

    DIFICULTAD_CHOICES = [
        ('Baja', 'Baja'),
        ('Media', 'Media'),
        ('Alta', 'Alta'),
    ]
    dificultad = models.CharField(
        max_length=50,
        choices=DIFICULTAD_CHOICES,
        default='Media',
        verbose_name='Dificultad'
    )
    tiempo_preparacion = models.IntegerField(default=0, verbose_name='Tiempo de preparación (min)')
    porciones = models.IntegerField(default=1, verbose_name='Porciones')
    es_vegetariano = models.BooleanField(default=False, verbose_name='¿Es vegetariano?')
    precio_referencia = models.IntegerField(default=0, verbose_name='Precio referencia (CLP)')
    # Guardamos los ingredientes como texto separado por comas
    ingredientes = models.TextField(
        blank=True,
        default='',
        verbose_name='Ingredientes',
        help_text='Ingredientes separados por coma (ej: Carne, Cebolla, Huevo)'
    )

    class Meta:
        verbose_name = 'Plato Típico'
        verbose_name_plural = 'Platos Típicos'
        ordering = ['id']

    def __str__(self):
        return self.nombre

    def get_ingredientes_lista(self):
        """Retorna los ingredientes como una lista de strings."""
        if self.ingredientes:
            return [i.strip() for i in self.ingredientes.split(',')]
        return []
