from django.db import models
from django.db.models import Avg
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
class Project (models.Model):
    name=models.CharField(max_length=50)
# Create your models here.

class TipoCocina(models.Model):
    Nombre=models.CharField(max_length=25)
    def __str__(self):
        return self.Nombre
    
    
class CategoriaL(models.Model):
    Nombre=models.CharField(max_length=30)
    def __str__(self):
        return self.Nombre
    

class Restaurante (models.Model):
    Nombre=models.CharField(max_length=50, default='Restaurante')
    Propietario=models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    Pais=models.CharField(max_length=50)
    Estado=models.CharField(max_length=50)
    Direccion=models.CharField(max_length=200)
    Promedio=models.DecimalField(max_digits=3,decimal_places=2, default=0, blank=True)
    TipoCocina=models.ForeignKey(TipoCocina,on_delete=models.CASCADE, blank=True, null=True)
    CategoriaL=models.ForeignKey(CategoriaL,on_delete=models.CASCADE, blank=True, null=True)
    Apertura=models.TimeField()
    Cierre=models.TimeField()
    Descripción=models.CharField(max_length=280, null=True, blank=True)
    def __str__(self):
        return (f"{self.Nombre}"
        f" - Propietario: {self.Propietario.username}" 
        f" - Promedio: {self.Promedio}"
        f" - País: {self.Pais}"
        f" - Estado: {self.Estado}"
        f" - Dirección: {self.Direccion}"
        f" - TipoCocina: {self.TipoCocina}"
        f" - CategoriaL: {self.CategoriaL}"
        f" - Apertura: {self.Apertura}"
        f" - Cierre: {self.Cierre}"
        f" - Descripción: {self.Descripción}")
    def calcular_promedio(self):
        resenas = Resena.objects.filter(RestauranteID=self)
        if resenas.exists():
            promedio = resenas.aggregate(promedio=Avg('Puntuacion'))['promedio']
            self.Promedio = round(promedio, 2)
        else:
            self.Promedio = 0

    
class FotosLugar(models.Model):
    RestauranteID=models.ForeignKey(Restaurante, on_delete=models.CASCADE, blank=True)
    Imagen=models.ImageField(upload_to='uploads/lugar', blank=True, null=True)

class Resena(models.Model):
    RestauranteID=models.ForeignKey(Restaurante,on_delete=models.CASCADE)
    UsuarioID=models.ForeignKey(User,on_delete=models.CASCADE)
    Fecha=models.DateField()
    Descripcion=models.CharField(max_length=280)
    Puntuacion=models.DecimalField(max_digits=2, decimal_places=1, validators=[MinValueValidator(1), MaxValueValidator(5)])
    def __str__(self):
        return (f"{self.RestauranteID.Nombre}"
        f" - Usuario: {self.UsuarioID.username}" 
        f" - Fecha: {self.Fecha}"
        f" - Descripcion: {self.Descripcion}"
        f" - Puntuacion: {self.Puntuacion}"
        )

@receiver(post_save, sender=Resena)
def actualizar_promedio_restaurante(sender, instance, **kwargs):
    restaurante = instance.RestauranteID
    restaurante.calcular_promedio()
    restaurante.save()

class FotosResena(models.Model):
    ResenaID=models.ForeignKey(Resena,on_delete=models.CASCADE)
    Imagen=models.ImageField(upload_to='uploads/resena', null=True, blank=True)
    
class FotoUsuario(models.Model):
    UsuarioID=models.ForeignKey(User, on_delete=models.CASCADE)
    Imagen=models.ImageField(upload_to='uploads/perfil', blank=True, null=True)
    