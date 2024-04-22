from django.urls import path
from .views import *

urlpatterns = [
    path('inicio/', go_home, name='inicio'),
    path('nuevo_producto/', crear_producto, name='crear_producto'),

]
