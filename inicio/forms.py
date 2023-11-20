from django import forms
from .models import FotosLugar,Restaurante

class FotosLugarForm(forms.ModelForm):
    class Meta:
        model=FotosLugar
        campo=['Imagen']

class RestauranteForm(forms.ModelForm):
    class Meta:
        model=Restaurante
        campos=('Pais','Estado','Direccion','TipoCocinaID','CategoriaL','Apertura','Cierre','Descripción')