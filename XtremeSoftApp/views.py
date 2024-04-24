from django.shortcuts import render, redirect
from .models import *

# Create your views here.

def go_home (request):
    return render(request,'inicio.html')

def mostrar_productos(request):
    lista_productos = Producto.objects.all()
    return render(request, "productos.html",  {'productos': lista_productos})

def crear_producto (request):
    if request.method=='GET':
        lista_productos=Producto.objects.all()
        return render(request,'crear_producto.html', {'productos': lista_productos})
    else:
        nuevo_producto = Producto()
        nuevo_producto.nombre=request.POST.get("name")
        nuevo_producto.descripcion = request.POST.get("descripcion")
        nuevo_producto.precio = float(request.POST.get("price"))
        nuevo_producto.foto = request.POST.get("image")
        nuevo_producto.save()
        return redirect("/lista_productos")






