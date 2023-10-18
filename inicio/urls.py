from django.urls import path
from . import views
urlpatterns=[
path('',views.crear_cuenta, name='crear_cuenta'),
path('iniciosesion/',views.inicio_sesion, name='inicio_sesion'),
path('home/',views.home, name='home'),
path('cerrarsesion/',views.cerrar_sesion, name='cerrar_sesion')
]