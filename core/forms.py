from django import forms
from django.forms import fields
from .models import Usuarios

class NovoUsuario(forms.ModelForm):

    class Meta:
        model = Usuarios
        fields = ('idade', 'cidade')