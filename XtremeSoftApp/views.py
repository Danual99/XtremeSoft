from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect
from .models import *

# Create your views here.

def inicio (request):
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

def mostrar_registro(request):
    return render(request, 'registro.html')


def registro_usuario(request):
    if request.method == 'GET':
        return render(request, 'registro.html')
    else:
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        repeat_password = request.POST.get('repeat_password')

        errors = []
        if password != repeat_password:
            errors.append("Las contraseñas no coinciden")

        existe_usuario =Usuario.objects.filter(username=username).exists()
        if existe_usuario:
            errors.append("Ya existe un usuario con ese nombre")

        existe_email = Usuario.objects.filter(email=email).exists()

        if existe_email:
            errors.append("Ya existe un usuario con ese email")

        if len(errors) != 0:
            return render(request, 'registro.html', {"errores":errors, "username": username, "email":email})
        else:
            user = Usuario.objects.create(username=username, password=make_password(password), email=email)
            user.save()
            return redirect('do_login')


def do_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('inicio')
        else:
            return render(request, 'inicio_sesion.html', {"error": "No ha sido posible iniciar sesión"})

    return render(request, "inicio_sesion.html")

def do_logout(request):
    logout(request)
    return redirect('inicio')
