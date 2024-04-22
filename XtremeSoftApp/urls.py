from django.urls import path
from .views import *

urlpatterns = [
    path('inicio/', go_home, name='inicio'),
    path('nuevo_producto/', crear_producto, name='crear_producto'),
    path('lista_productos/', mostrar_productos, name='mostrar_productos'),

]
