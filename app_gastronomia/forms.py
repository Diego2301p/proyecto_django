"""
app_gastronomia/forms.py - Formularios Django para CRUD de platos típicos.

Proporciona el formulario ModelForm para crear y editar platos típicos chilenos.
"""

from django import forms
from .models import PlatoTipico


class PlatoTipicoForm(forms.ModelForm):
    """Formulario para crear y editar platos típicos."""
    class Meta:
        model = PlatoTipico
        fields = ['nombre', 'region', 'descripcion', 'imagen', 'dificultad',
                  'tiempo_preparacion', 'porciones', 'es_vegetariano',
                  'precio_referencia', 'ingredientes']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'region': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'imagen': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'nombre_imagen.jpg'
            }),
            'dificultad': forms.Select(attrs={'class': 'form-control'}),
            'tiempo_preparacion': forms.NumberInput(attrs={
                'class': 'form-control', 'min': 0,
                'placeholder': 'Minutos'
            }),
            'porciones': forms.NumberInput(attrs={
                'class': 'form-control', 'min': 1
            }),
            'es_vegetariano': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'precio_referencia': forms.NumberInput(attrs={
                'class': 'form-control', 'min': 0
            }),
            'ingredientes': forms.Textarea(attrs={
                'class': 'form-control', 'rows': 3,
                'placeholder': 'Carne, Cebolla, Huevo, Aceitunas'
            }),
        }

    def clean_tiempo_preparacion(self):
        """Validación: el tiempo debe ser positivo."""
        tiempo = self.cleaned_data.get('tiempo_preparacion')
        if tiempo is not None and tiempo < 0:
            raise forms.ValidationError('El tiempo de preparación no puede ser negativo.')
        return tiempo

