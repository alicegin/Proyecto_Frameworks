from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login,logout, authenticate
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.db import IntegrityError
from .forms import RestauranteForm,FotosLugarForm
from .models import Restaurante,FotosLugar
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
    submitted = False

    if request.user.is_authenticated:
        if request.method == 'POST':
            InfoForm = RestauranteForm(request.POST)
            FotoForm = FotosLugarForm(request.POST)

            if InfoForm.is_valid():
                restaurante = InfoForm.save(commit=False)
                restaurante.Propietario = request.user
                restaurante.save()

                if 'Imagen' in request.FILES:
                    for imagen in request.FILES.getlist('Imagen'):
                        FotosLugar.objects.create(RestauranteID=restaurante, Imagen=imagen)


                messages.success(request, ("El restaurante fue creado"))
                return HttpResponseRedirect('/crearrestaurante?submitted=True')
        else:
            InfoForm = RestauranteForm()
            FotoForm = FotosLugarForm()

            if 'submitted' in request.GET:
                submitted = True

        return render(request, 'crear_restaurante.html', {'InfoForm': InfoForm, 'FotoForm': FotoForm, 'submitted': submitted})
    else:
        # Manejar el caso en que el usuario no esté autenticado (puedes redirigirlo o mostrar un mensaje)
        return render(request, 'error.html', {'mensaje': 'Acceso no autorizado'})
    
def mis_restaurantes(request):
    if request.user.is_authenticated:
        Elementos=Restaurante.objects.filter(Propietario=request.user).prefetch_related('fotoslugar_set')
    return render(request, "mis_restaurantes.html",{'Elementos': Elementos})

def eliminar_restaurante(request,pk):
    if request.user.is_authenticated:
        restaurante=get_object_or_404(Restaurante,id=pk)
        if request.user.username== restaurante.Propietario.username:
            restaurante.delete()
            messages.success(request,"El restaurante ha sido eliminado")
            return redirect(request.META.get("HTTP_REFERER"))
        else:
            return redirect(request.META.get("HTTP_REFERER"))
       