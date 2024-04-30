from django.contrib.auth.hashers import make_password
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
    lista_campos = Campo_Tiro.objects.all()
    return render(request, "campos.html",  {'campos': lista_campos})

def crear_campo (request):
    if request.method=='GET':
        lista_campos = Campo_Tiro.objects.all()
        return render(request,'crear_campo_tiro.html', {'campos': lista_campos})
    else:
        nuevo_campo = Campo_Tiro()
        nuevo_campo.nombre=request.POST.get("name")
        nuevo_campo.aforo = request.POST.get("aforo")
        nuevo_campo.localizacion = float(request.POST.get("price"))
        nuevo_campo.foto = request.POST.get("image")
        nuevo_campo.save()
        return redirect("/lista_productos")


def registro_usuario(request):
    if request.method == 'GET':
        return render(request, 'registro.html')
    else:
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        repeat_password = request.POST.get('password_repeat')

        errors = []
        if password == repeat_password:
            errors.append("Las contraseñas no coinciden")

        existe_usuario =Usuario.objects.filter(username=username).exists()
        if existe_usuario:
            errors.append("Ya existe un usuario con ese nombre")

        existe_email = Usuario.objects.filter(password=password).exists()
        errors.append("Ya existe un usuario con ese email")

        if len(errors) != 0:
            return render(request, 'registro.html', {"errores":errors, "username": username, "email":email})
        else:
            user = Usuario.objects.create(username=username, password=make_password(password), email=email)
            user.save()
            return redirect('inicio.html')

