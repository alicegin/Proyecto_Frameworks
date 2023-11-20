from django import forms
from .models import Restaurante, FotosLugar,TipoCocina,CategoriaL


class RestauranteForm(forms.ModelForm):
    class Meta:
        model=Restaurante
        fields=('Pais','Estado','Direccion','Apertura','Cierre','Descripción')

class FotosLugarForm(forms.ModelForm):
    class Meta:
        model=FotosLugar
        fields=['Imagen']