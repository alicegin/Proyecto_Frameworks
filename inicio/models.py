from django.db import models
from django.contrib.auth.models import User
class Project (models.Model):
    name=models.CharField(max_length=50)
# Create your models here.

class TipoCocina(models.Model):
    Nombre=models.CharField(max_length=25)
    
    
class CategoriaL(models.Model):
    Nombre=models.CharField(max_length=30)
    

class Restaurante (models.Model):
    Propietario=models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    Pais=models.CharField(max_length=50)
    Estado=models.CharField(max_length=50)
    Direccion=models.CharField(max_length=200)
    Promedio=models.DecimalField(max_digits=3,decimal_places=3, default=0)
    TipoCocinaID=models.ForeignKey(TipoCocina,on_delete=models.CASCADE)
    CategoriaL=models.ForeignKey(CategoriaL,on_delete=models.CASCADE)
    Apertura=models.TimeField()
    Cierre=models.TimeField()
    Descripción=models.CharField(max_length=280)
    
class FotosLugar(models.Model):
    RestauranteID=models.ForeignKey(Restaurante, on_delete=models.CASCADE)
    Imagen=models.ImageField(upload_to='uploads/lugar', null=True)

class Resena(models.Model):
    RestauranteID=models.ForeignKey(Restaurante,on_delete=models.CASCADE)
    UsuarioID=models.ForeignKey(User,on_delete=models.CASCADE)
    Fecha=models.DateField()
    Descripcion=models.CharField(max_length=280)
    Puntuacion=models.IntegerField()

class FotosResena(models.Model):
    ResenaID=models.ForeignKey(Resena,on_delete=models.CASCADE)
    Imagen=models.ImageField(upload_to='uploads/resena', null=True)