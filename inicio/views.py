from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login,logout, authenticate
from django.http import HttpResponseRedirect
from django.db import IntegrityError
from .forms import RestauranteForm
# Create your views here.
def inicio_sesion(request):
    if request.method == 'GET':
        return render(request, 'inicio_sesion.html', {
            'form': AuthenticationForm
        })
    else:
        usuario= authenticate(request, username=request.POST['Usuario'], password=request.POST['Contrasena'])
        if usuario is None:
            return render(request,'inicio_sesion.html', {
                'form': AuthenticationForm,
                'error': '<div class="alert alert-danger" role="alert">Contraseña o usuario inválido </div>'
            })
        else:
            login(request,usuario)
            return redirect('home')

def cerrar_sesion(request):
    logout(request)
    return redirect("inicio_sesion")
    
def home(request):
    return render(request,'home.html')

def crear_cuenta(request):
    if request.method=='GET':
        return render(request, 'crear_cuenta.html', {
            'form': UserCreationForm
        })
    else:
        try:
            usuario=User.objects.create_user(username=request.POST['Usuario'],password=request.POST['Contrasena'], 
            email=request.POST['Correo'])
            usuario.save()
            login(request,usuario)
            return redirect('home')
        except IntegrityError:
            return render(request, 'crear_cuenta.html', {
            'form': UserCreationForm,
            'error': '<div class="alert alert-danger" role="alert">El usuario ya existe. Intente con uno nuevo. </div>'
        })

def crear_restaurante(request):
    submitted=False
    if request.method =="POST":
        InfoForm =RestauranteForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/crearr?submitted=True')
    else:
          form=RestauranteForm
          if 'submitted' in request.GET:
              submitted=True
    return render(request,'crear_restaurante.html',{'InfoForm': InfoForm, 'submitted':submitted})
       