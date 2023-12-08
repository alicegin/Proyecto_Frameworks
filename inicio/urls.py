from django.urls import path
from . import views
urlpatterns=[
path('',views.crear_cuenta, name='crear_cuenta'),
path('iniciosesion/',views.inicio_sesion, name='inicio_sesion'),
path('home/',views.home, name='home'),
path('cerrarsesion/',views.cerrar_sesion, name='cerrar_sesion'),
path('crearrestaurante/',views.crear_restaurante, name='crear_restaurante'),
path('misrestaurantes/',views.mis_restaurantes, name='mis_restaurantes'),
path('eliminarrestaurante/<int:pk>',views.eliminar_restaurante, name='eliminar_restaurante'),
path('editarrestaurante/<int:pk>',views.editar_restaurante, name='editar_restaurante'),
path('eliminarimagen/<int:pk>',views.eliminar_imagen_res, name='eliminar_imagen_res'),
path('micuenta/',views.mi_cuenta, name='mi_cuenta'),
path('elegirrestaurante/',views.elegir_restaurante, name='elegir_restaurante'),
path('crearresena/ <int:pk>',views.crear_resena, name='crear_resena'),
path('misresenas/',views.mis_resenas, name='mis_resenas'),
path('eliminarresena/<int:pk>',views.eliminar_resena, name='eliminar_resena'),
path('editarresena/<int:pk>',views.editar_resena, name='editar_resena'),
path('explorar/',views.explorar, name='explorar'),
path('restaurante/<int:pk>',views.restaurante, name='restaurante'),
path('eliminartodasimg/<int:pk>',views.eliminar_todas_imagen_res, name='eliminar_todas_imagen_res')
]