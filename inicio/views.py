from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login,logout, authenticate
# Create your views here.
def inicio_sesion(request):
    if request.method == 'GET':
        return render(request, 'inicio_sesion.html', {
            'form': AuthenticationForm
        })
    else:
        usuario= authenticate(request, usuario=request.POST['Usuario'], password=request.POST['Contrasena'])
        if usuario is None:
            return render(request,'inicio_sesion.html', {
                'form': AuthenticationForm,
                'Error': '<div class="alert alert-danger" role="alert">Contraseña o usuario inválido </div>'
            })
        else:
            login(request,usuario)
            return redirect('home')
    
def home(request):
    return render(request,'home.html')