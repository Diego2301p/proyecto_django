"""
app_turismo/models.py - Modelos ORM de la aplicación de destinos turísticos.

Define el modelo DestinoTuristico que representa un destino turístico
de Chile en la base de datos MySQL. Reemplaza la lectura de datos
desde archivos JSON por el ORM de Django.
"""

from django.db import models


class DestinoTuristico(models.Model):
    """
    Modelo que representa un destino turístico de Chile.

    Campos:
        nombre (str): Nombre del destino (ej: "Torres del Paine").
        region (str): Región de Chile donde se ubica.
        descripcion (str): Descripción detallada del destino.
        imagen (str): Nombre del archivo de imagen en static/img/.
        categoria (str): Categoría del destino (Naturaleza, Cultura, Aventura).
        precio_estimado (int): Precio estimado en pesos chilenos.
        puntuacion (float): Puntuación del destino (1.0 a 5.0).
        destacado (bool): Si el destino aparece en la sección de destacados.
        actividades (str): Actividades disponibles, separadas por coma.
    """
    nombre = models.CharField(max_length=200, verbose_name='Nombre')
    region = models.CharField(max_length=200, verbose_name='Región')
    descripcion = models.TextField(verbose_name='Descripción')
    imagen = models.CharField(max_length=200, verbose_name='Imagen')
    categoria = models.CharField(max_length=100, verbose_name='Categoría')
    precio_estimado = models.IntegerField(default=0, verbose_name='Precio estimado (CLP)')
    puntuacion = models.FloatField(default=0.0, verbose_name='Puntuación')
    destacado = models.BooleanField(default=False, verbose_name='Destacado')
    # Guardamos las actividades como texto separado por comas
    # para mantener simplicidad (alternativa: modelo ManyToMany)
    actividades = models.TextField(
        blank=True,
        default='',
        verbose_name='Actividades',
        help_text='Actividades separadas por coma (ej: Trekking, Fotografía, Kayak)'
    )

    class Meta:
        verbose_name = 'Destino Turístico'
        verbose_name_plural = 'Destinos Turísticos'
        ordering = ['id']

    def __str__(self):
        return self.nombre

    def get_actividades_lista(self):
        """Retorna las actividades como una lista de strings."""
        if self.actividades:
            return [a.strip() for a in self.actividades.split(',')]
        return []
