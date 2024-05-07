from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect
from .models import *
from  django.contrib.auth import authenticate, login, logout
from .decorators import *
# Create your views here.

def inicio (request):
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


def crear_empleado (request):
    if request.method == 'GET':
        lista_campos = Campo_Tiro.objects.all()
        return render(request, 'crear_empleado.html',{'campos':lista_campos})
    else:
        empleado = Empleado()
        empleado.nombre = request.POST.get('name_emp')
        empleado.fecha_nacimiento = request.POST.get('date_emp')
        empleado.codigo = request.POST.get('code_emp')

        empleado.mail = request.POST.get('mail_emp')
        empleado.image_url = request.POST.get('image_emp')

        empleado.save()

        campos = request.POST.getlist('campos')

        for c in campos:
            campo = Campo_Tiro.objects.get(id=c)
            empleado.campos.add(campo)


        return redirect('/lista_empleados/')
@check_user_role('EMP')
def ver_empleados(request):
    lista_empleados = Empleado.objects.all()
    return render(request, 'empleados.html' ,{'empleados':lista_empleados})

def editar_empleado (request, id):
    if request.method == 'GET':
        empleado = Empleado.objects.get(id=id)
        campos = Campo_Tiro.objects.all()
        ids_cammpos = empleado.campos.values_list('id', flat=True)

        return render(request, 'crear_empleado.html', {'empleado':empleado, 'campos':campos, 'ids_campos':ids_cammpos})
    else:
        empleado = Empleado()
        empleado.id = id
        empleado.nombre = request.POST.get('name_emp')
        empleado.fecha_nacimiento = request.POST.get('date_emp')
        empleado.codigo = request.POST.get('code_emp')
        empleado.mail= request.POST.get('mail_emp')
        empleado.image_url = request.POST.get('image_emp')
        Empleado.save(empleado)


        return redirect('/lista_empleados')

def eliminar_empleado(request, id):
    empleado = Empleado.objects.get(id=id)
    if empleado is not None:
        Empleado.delete(empleado)
        return redirect('/lista_empleados')



def crear_usuario_empleado(request, id):
    empleado = Empleado.objects.get(id=id)

    if empleado.usuario is None:
        usuario = Usuario()
        usuario.username = empleado.nombre.replace(" ","_")
        usuario.email = empleado.mail
        usuario.password = make_password(empleado.codigo)
        usuario.rol = Rol.EMPLOYEE
        usuario.save()

        empleado.usuario = usuario
        empleado.save()
        return redirect('do_login')
    else:
        return redirect('lista_empleados/')



def mostrar_registro(request):
    return render(request, 'registro.html')

def mostrar_campos(request):
    lista_campos = Campo_Tiro.objects.all()
    return render(request, "campos.html",  {'campos': lista_campos})

def crear_campo (request):
    if request.method=='GET':
        lista_campos = Campo_Tiro.objects.all()
        return render(request,'crear_campo_tiro.html', {'campos': lista_campos})
    else:
        nuevo_campo = Campo_Tiro()
        nuevo_campo.nombre = request.POST.get("nombre")
        nuevo_campo.aforo = int(request.POST.get("aforo"))
        nuevo_campo.localizacion = request.POST.get("localizacion")
        nuevo_campo.image = request.POST.get("image")
        nuevo_campo.save()
        return redirect("/lista_campos")

def editar_campo (request,id):
    if request.method == 'GET':
        campos = Campo_Tiro.objects.get(id=id)
        return render(request, 'crear_campo_tiro.html', {'campos': campos})
    else:
        campos = Campo_Tiro()
        campos.id = id
        campos.nombre = request.POST.get("nombre")
        campos.aforo = int(request.POST.get("aforo"))
        campos.localizacion = request.POST.get("localizacion")
        campos.image = request.POST.get("image")
        Campo_Tiro.save(campos)
        return redirect('/lista_campos')

def eliminar_campo(request, id):
    campo = Campo_Tiro.objects.get(id=id)
    if campo is not None:
        Campo_Tiro.delete(campo)
        return redirect('/lista_campos')



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
            return redirect('inicio')


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

def acceso_denegado(request):
    return render(request, 'acceso_denegado.html')

