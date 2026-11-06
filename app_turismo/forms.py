"""
app_turismo/forms.py - Formularios Django para CRUD de destinos y reservas.

Proporciona formularios ModelForm para:
- DestinoTuristicoForm: Crear y editar destinos turísticos.
- ReservaTuristicaForm: Crear y editar reservas turísticas (transacción).
"""

from datetime import date

from django import forms
from .models import DestinoTuristico, ReservaTuristica


class DestinoTuristicoForm(forms.ModelForm):
    """Formulario para crear y editar destinos turísticos."""
    class Meta:
        model = DestinoTuristico
        fields = ['nombre', 'region', 'descripcion', 'imagen', 'categoria',
                  'precio_estimado', 'puntuacion', 'destacado', 'actividades']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'region': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'imagen': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'nombre_imagen.jpg'
            }),
            'categoria': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Naturaleza, Cultura, Aventura'
            }),
            'precio_estimado': forms.NumberInput(attrs={
                'class': 'form-control', 'min': 0
            }),
            'puntuacion': forms.NumberInput(attrs={
                'class': 'form-control', 'min': 0, 'max': 5, 'step': '0.1'
            }),
            'destacado': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'actividades': forms.Textarea(attrs={
                'class': 'form-control', 'rows': 3,
                'placeholder': 'Trekking, Fotografía, Kayak'
            }),
        }


class ReservaTuristicaForm(forms.ModelForm):
    """
    Formulario para crear y editar reservas turísticas.
    Transacción que involucra múltiples entidades relacionadas.
    """
    class Meta:
        model = ReservaTuristica
        fields = ['destino', 'plato', 'fecha_reserva', 'num_personas',
                  'estado', 'observaciones']
        widgets = {
            'destino': forms.Select(attrs={'class': 'form-control'}),
            'plato': forms.Select(attrs={'class': 'form-control'}),
            'fecha_reserva': forms.DateInput(attrs={
                'class': 'form-control', 'type': 'date'
            }),
            'num_personas': forms.NumberInput(attrs={
                'class': 'form-control', 'min': 1, 'max': 50
            }),
            'estado': forms.Select(attrs={'class': 'form-control'}),
            'observaciones': forms.Textarea(attrs={
                'class': 'form-control', 'rows': 3,
                'placeholder': 'Alguna observación especial para la reserva...'
            }),
        }

    def clean_num_personas(self):
        """Validación: el número de personas debe estar entre 1 y 50."""
        num = self.cleaned_data.get('num_personas')
        if num is not None and num < 1:
            raise forms.ValidationError('Debe haber al menos 1 persona.')
        if num is not None and num > 50:
            raise forms.ValidationError('El máximo permitido es de 50 personas por reserva.')
        return num

    def clean_fecha_reserva(self):
        """Validación: una reserva nueva no puede tener fecha en el pasado."""
        fecha = self.cleaned_data.get('fecha_reserva')
        if fecha and not self.instance.pk and fecha < date.today():
            raise forms.ValidationError('La fecha de la reserva no puede ser anterior a hoy.')
        return fecha

    def clean(self):
        """Validación cruzada: no se puede confirmar una reserva con fecha pasada."""
        cleaned = super().clean()
        fecha = cleaned.get('fecha_reserva')
        estado = cleaned.get('estado')
        if fecha and estado == 'Pendiente' and fecha < date.today() and self.instance.pk:
            self.add_error('estado', 'Una reserva con fecha pasada no puede quedar Pendiente.')
        return cleaned

