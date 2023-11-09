from django.contrib import admin
from .models import Resena,Restaurante,FotosLugar,FotosResena, TipoCocina, CategoriaL
# Register your models here.
admin.site.register(Resena)
admin.site.register(Restaurante)
admin.site.register(FotosLugar)
admin.site.register(FotosResena)
admin.site.register(TipoCocina)
admin.site.register(CategoriaL)
