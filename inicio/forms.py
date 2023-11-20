from django import forms
from .models import Restaurante, FotosLugar,TipoCocina,CategoriaL


class RestauranteForm(forms.ModelForm):
    class Meta:
        model=Restaurante
        fields=('Nombre','Pais','Estado','TipoCocina','CategoriaL','Direccion','Apertura','Cierre','Descripción')
        widgets = {
            'Nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'Pais': forms.TextInput(attrs={'class': 'form-control'}),
            'Estado': forms.TextInput(attrs={'class': 'form-control'}),
            'TipoCocina': forms.Select(attrs={'class': 'form-control'}),
            'CategoriaL': forms.Select(attrs={'class': 'form-control'}),
            'Direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'Apertura': forms.TimeInput(format='%H:%M', attrs={'class': 'form-control'}),
            'Cierre': forms.TimeInput(format='%H:%M', attrs={'class': 'form-control'}),
            'Descripción': forms.TextInput(attrs={'class': 'form-control'}),
        }

class FotosLugarForm(forms.ModelForm):
    class Meta:
        model=FotosLugar
        fields=['Imagen']