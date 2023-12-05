from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login,logout, authenticate
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.db import IntegrityError
from .forms import RestauranteForm,FotosLugarForm, FotoUsuarioForm, ResenaForm, FotoResenaForm
from .models import Restaurante,FotosLugar,FotoUsuario, FotosResena, Resena
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
    if request.user.is_authenticated:
        usuario = request.user
        foto = FotoUsuario.objects.filter(UsuarioID=usuario).first()
        restaurantes=Restaurante.objects.all().prefetch_related('fotoslugar_set')
        return render(request,'home.html',{'usuario':usuario,'foto':foto, 'restaurantes': restaurantes})

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
        usuario = request.user
        foto = FotoUsuario.objects.filter(UsuarioID=usuario).first()
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

        return render(request, 'crear_restaurante.html', {'InfoForm': InfoForm, 'FotoForm': FotoForm, 'submitted': submitted, 'usuario':usuario,'foto':foto})
    else:
        # Manejar el caso en que el usuario no esté autenticado 
        return render(request, 'error.html', {'mensaje': 'Acceso no autorizado'})
    
def mis_restaurantes(request):
    if request.user.is_authenticated:
        usuario = request.user
        foto = FotoUsuario.objects.filter(UsuarioID=usuario).first()
        
        Elementos=Restaurante.objects.filter(Propietario=request.user).prefetch_related('fotoslugar_set')
    return render(request, "mis_restaurantes.html",{'Elementos': Elementos, 'usuario':usuario,'foto':foto})

def eliminar_restaurante(request,pk):
    if request.user.is_authenticated:
        restaurante=get_object_or_404(Restaurante,id=pk)
        if request.user.username== restaurante.Propietario.username:
            restaurante.delete()
            messages.success(request,"El restaurante ha sido eliminado")
            return redirect(request.META.get("HTTP_REFERER"))
        else:
            return redirect(request.META.get("HTTP_REFERER"))

def editar_restaurante(request, pk):
    if request.user.is_authenticated:
        usuario = request.user
        foto = FotoUsuario.objects.filter(UsuarioID=usuario).first()
        restaurante=get_object_or_404(Restaurante,id=pk)
        if request.user.username== restaurante.Propietario.username:
    # Obtener todas las fotos asociadas al restaurante
            fotos = FotosLugar.objects.filter(RestauranteID=restaurante.id)

            InfoForm = RestauranteForm(request.POST or None, instance=restaurante)
            FotoForm = FotosLugarForm(request.POST or None, request.FILES or None)

            if request.method == 'POST':
                if InfoForm.is_valid() and FotoForm.is_valid():
                    restaurante = InfoForm.save(commit=False)
                    restaurante.Propietario = request.user
                    restaurante.save()

                    # Eliminar fotos existentes del restaurante
                    #FotosLugar.objects.filter(RestauranteID=restaurante.id).delete()

                    # Guardar las nuevas fotos
                    for imagen in request.FILES.getlist('Imagen'):
                        FotosLugar.objects.create(RestauranteID=restaurante, Imagen=imagen)

                    messages.success(request, "El restaurante fue actualizado")
                    return redirect('mis_restaurantes')

            return render(request, "editar_restaurante.html", {'InfoForm': InfoForm, 'FotoForm': FotoForm, 'restaurante': restaurante, 'fotos': fotos,'usuario':usuario,'foto':foto})

def eliminar_imagen_res(request, pk):
    foto = get_object_or_404(FotosLugar, id=pk)
    foto.delete()
    return redirect(request.META.get("HTTP_REFERER"))

def mi_cuenta(request):
    if request.user.is_authenticated:
        usuario = request.user
        foto = FotoUsuario.objects.filter(UsuarioID=usuario).first()

        if request.method == 'GET':
            FotoForm = FotoUsuarioForm()
            return render(request, "mi_cuenta.html", {'usuario': usuario, 'foto': foto, 'FotoForm': FotoForm})
        elif request.method == 'POST':
            try:
                FotoForm = FotoUsuarioForm(request.POST)
                usuario.first_name = request.POST['Nombre']
                usuario.last_name = request.POST['Apellido']
                usuario.username = request.POST['Username']
                usuario.email = request.POST['Correo']
                usuario.save()

                # Manejar la foto si se está cargando una nueva
                if request.FILES.get('archivo'):
                    if foto is None:
                        foto = FotoUsuario(UsuarioID=usuario)  # Crea un nuevo objeto si no existe
                    foto.Imagen = request.FILES.get('archivo')
                    foto.save()

                return render(request, "mi_cuenta.html", {'usuario': usuario, 'foto': foto, 'FotoForm': FotoForm})
            except IntegrityError:
                return render(request, 'mi_cuenta.html', {
                    'usuario': usuario, 'foto': foto,
                    'error': '<div class="alert alert-danger" role="alert">El usuario ya existe. Intente con uno nuevo. </div>'
                })
def crear_resena(request, pk):
    if request.user.is_authenticated:
        usuario = request.user
        foto = FotoUsuario.objects.filter(UsuarioID=usuario).first()
        restaurante=get_object_or_404(Restaurante,id=pk)
        if request.user.username!= restaurante.Propietario.username:
            if request.method == 'GET':
                InfoForm = ResenaForm()
                FotoForm = FotosResena()
                return render(request, "crear_resena.html", {'usuario': usuario, 'foto': foto, 'FotoForm': FotoForm, 'InfoForm': InfoForm})
            elif request.method == 'POST':
                InfoForm = ResenaForm(request.POST)
                FotoForm = FotoResenaForm(request.POST)
                if InfoForm.is_valid() and FotoForm.is_valid():
                        
                        informacion = InfoForm.save(commit=False)
                        informacion.Puntuacion= request.POST['Puntuacion']
                        informacion.RestauranteID= restaurante
                        informacion.UsuarioID = usuario
                        informacion.Fecha= timezone.now()
                        informacion.save()

                        if 'Imagen' in request.FILES:
                            for imagen in request.FILES.getlist('Imagen'):
                                FotosResena.objects.create(ResenaID=informacion, Imagen=imagen)

                        messages.success(request, "Se ha creado la reseña")
                        return redirect('elegir_restaurante')
        else:
            messages.error(request,'No puedes hacer reseñas de tu propio restaurante')
            return redirect(request.META.get("HTTP_REFERER"))

def elegir_restaurante(request):
    if request.user.is_authenticated:
        usuario = request.user
        foto = FotoUsuario.objects.filter(UsuarioID=usuario).first()
        Elementos=Restaurante.objects.all().exclude(Propietario=usuario).prefetch_related('fotoslugar_set')
        return render (request, "elegir_restaurante.html",{'Elementos': Elementos, 'usuario':usuario,'foto':foto})

def mis_resenas(request):
    if request.user.is_authenticated:
        usuario = request.user
        foto = FotoUsuario.objects.filter(UsuarioID=usuario).first()
        resenas=Resena.objects.filter(UsuarioID=usuario).prefetch_related('fotosresena_set')
        restaurantes = Restaurante.objects.filter(id__in=resenas.values('RestauranteID')).prefetch_related('fotoslugar_set')
        return render(request, 'mis_resenas.html',{'usuario':usuario,'foto':foto, 'resenas': resenas, 'restaurantes': restaurantes})

def eliminar_resena(request,pk):
    if request.user.is_authenticated:
        resena=get_object_or_404(Resena,id=pk)
        if request.user.username== resena.UsuarioID.username:
            resena.delete()
            messages.success(request,"La reseña ha sido eliminada")
            return redirect(request.META.get("HTTP_REFERER"))
        else:
            return redirect(request.META.get("HTTP_REFERER"))

def editar_resena (request, pk):
    if request.user.is_authenticated:
        usuario = request.user
        foto = FotoUsuario.objects.filter(UsuarioID=usuario).first()
        resena=get_object_or_404(Resena,id=pk)
        restaurante = get_object_or_404(Restaurante, id=resena.RestauranteID.id)
        if request.user.username== resena.UsuarioID.username:

            fotos = FotosResena.objects.filter(ResenaID=resena.id)

            InfoForm = ResenaForm(request.POST or None, instance=resena)
            FotoForm = FotoResenaForm(request.POST or None, request.FILES or None)

            if request.method == 'POST':
                print(request.POST)
                if InfoForm.is_valid() and FotoForm.is_valid():
                    resena = InfoForm.save(commit=False)
                    resena.Puntuacion= float(request.POST['Puntuacion'])
                    resena.RestauranteID= restaurante
                    resena.UsuarioID = usuario
                    resena.Fecha= timezone.now()
                    resena.save()

                    # Eliminar fotos existentes del restaurante
                    #FotosLugar.objects.filter(RestauranteID=restaurante.id).delete()

                    # Guardar las nuevas fotos
                    for imagen in request.FILES.getlist('Imagen'):
                        FotosResena.objects.create(ResenaID=resena, Imagen=imagen)

                    messages.success(request, "La resena fue actualizada")
                    return redirect('mis_resenas')
            else:
                return render(request, "editar_resena.html", {'InfoForm': InfoForm, 'FotoForm': FotoForm, 'resena': resena, 'fotos': fotos,'usuario':usuario,'foto':foto})
            
def explorar(request):
    if request.user.is_authenticated:
        usuario = request.user
        foto = FotoUsuario.objects.filter(UsuarioID=usuario).first()
        restaurantes = Restaurante.objects.all().prefetch_related('fotoslugar_set')
    return render(request, "explorar.html",{'usuario':usuario,'foto': foto, 'restaurantes': restaurantes})

def restaurante(request, pk):
    if request.user.is_authenticated:
        usuario = request.user
        foto = FotoUsuario.objects.filter(UsuarioID=usuario).first()
        restaurante = Restaurante.objects.filter(id=pk).first()
        fotoslugar = FotosLugar.objects.filter(RestauranteID=restaurante.id)
        resenas=Resena.objects.filter(RestauranteID=restaurante)
        foto_cresena = FotoUsuario.objects.filter(UsuarioID__in=resenas.values('UsuarioID')).first()
        foto_creador=FotoUsuario.objects.filter(UsuarioID=restaurante.Propietario).first()
    return render(request,'restaurante.html',{'usuario': usuario, 'foto': foto, 'resenas': resenas, 'restaurante': restaurante, 'foto_creador': foto_creador, 'fotoslugar': fotoslugar, 'foto_cresena': foto_cresena})
