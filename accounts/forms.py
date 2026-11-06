"""
accounts/forms.py - Formularios Django para la gestión de cuentas.

Incluye formularios para:
- Inicio de sesión (LoginForm).
- Creación de usuarios con asignación de grupo (UsuarioCrearForm).
- Edición de usuarios (UsuarioEditarForm).
"""

from django import forms
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm


class LoginForm(forms.Form):
    """Formulario de inicio de sesión con usuario y contraseña."""
    username = forms.CharField(
        label='Usuario',
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese su usuario',
            'autofocus': True,
        })
    )
    password = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese su contraseña',
        })
    )


class UsuarioCrearForm(UserCreationForm):
    """
    Formulario para crear un nuevo usuario con asignación de grupo.
    Extiende UserCreationForm de Django para agregar campos adicionales.
    """
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
        label='Correo electrónico'
    )
    first_name = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Nombre'
    )
    last_name = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Apellido'
    )
    grupo = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Perfil / Grupo',
        empty_label='-- Seleccione un perfil --'
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Agregar clase Bootstrap a los campos heredados
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})

    def save(self, commit=True):
        user = super().save(commit=commit)
        if commit:
            grupo = self.cleaned_data['grupo']
            user.groups.clear()
            user.groups.add(grupo)
        return user


class UsuarioEditarForm(forms.ModelForm):
    """
    Formulario para editar un usuario existente.
    Permite cambiar nombre, apellido, email, grupo y estado activo.
    """
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
        label='Correo electrónico'
    )
    first_name = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Nombre'
    )
    last_name = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Apellido'
    )
    grupo = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Perfil / Grupo',
        empty_label='-- Seleccione un perfil --'
    )
    is_active = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        label='Usuario activo'
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'is_active']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        # Preseleccionar el grupo actual del usuario
        if self.instance.pk:
            grupos = self.instance.groups.all()
            if grupos.exists():
                self.fields['grupo'].initial = grupos.first()

    def save(self, commit=True):
        user = super().save(commit=commit)
        if commit:
            grupo = self.cleaned_data['grupo']
            user.groups.clear()
            user.groups.add(grupo)
        return user

