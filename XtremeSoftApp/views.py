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
        return render(request,'crear_producto.html', {'campos': lista_productos})
    else:
        nuevo_producto = Producto()
        nuevo_producto.nombre=request.POST.get("name")
        nuevo_producto.descripcion = request.POST.get("descripcion")
        nuevo_producto.precio = float(request.POST.get("price"))
        nuevo_producto.foto = request.POST.get("image")
        nuevo_producto.save()
        return redirect("/lista_productos")


def editar_producto (request, id):
    if request.method == 'GET':
        producto = Producto.objects.get(id=id)
        return render(request, 'crear_producto.html', {'producto':producto})
    else:
        producto = Producto()
        producto.id = id
        producto.nombre = request.POST.get('name')
        producto.descripcion = request.POST.get('descripcion')
        producto.precio = float(request.POST.get('price'))
        producto.foto = request.POST.get('image')
        Producto.save(producto)
        return redirect('/lista_productos')


def eliminar_producto(request, id):
    producto = Producto.objects.get(id=id)
    if producto is not None:
        Producto.delete(producto)
        return redirect('/lista_productos')


def mostrar_campos(request):
    lista_campos = Producto.objects.all()
    return render(request, "campos.html",  {'campos': lista_campos})
#
# def crear_producto (request):
#     if request.method=='GET':
#         lista_productos=Producto.objects.all()
#         return render(request,'crear_producto.html', {'productos': lista_productos})
#     else:
#         nuevo_producto = Producto()
#         nuevo_producto.nombre=request.POST.get("name")
#         nuevo_producto.descripcion = request.POST.get("descripcion")
#         nuevo_producto.precio = float(request.POST.get("price"))
#         nuevo_producto.foto = request.POST.get("image")
#         nuevo_producto.save()
#         return redirect("/lista_productos")
#
#
# def editar_producto (request, id):
#     if request.method == 'GET':
#         producto = Producto.objects.get(id=id)
#         return render(request, 'crear_producto.html', {'producto':producto})
#     else:
#         producto = Producto()
#         producto.id = id
#         producto.nombre = request.POST.get('name')
#         producto.descripcion = request.POST.get('descripcion')
#         producto.precio = float(request.POST.get('price'))
#         producto.foto = request.POST.get('image')
#         Producto.save(producto)
#         return redirect('/lista_productos')
#
#
# def eliminar_producto(request, id):
#     producto = Producto.objects.get(id=id)
#     if producto is not None:
#         Producto.delete(producto)
#         return redirect('/lista_productos')
#
#
#
#
