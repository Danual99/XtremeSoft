from datetime import date

from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import *
from  django.contrib.auth import authenticate, login, logout
from .carrito import *
import random
import string
from django.contrib import messages

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

def buscar_productos(request):
    nombre = request.GET.get("buscar")
    productos = Producto.objects.filter(nombre__icontains=nombre)

    return render(request, 'productos.html', {'productos': productos})


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

        lista_campos = request.POST.getlist('campos')
        empleado.campos.clear()
        for c in lista_campos:
            campo = Campo_Tiro.objects.get(id=c)
            empleado.campos.add(campo)


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

def buscar_campos(request):
    nombre = request.GET.get("buscar")
    campos = Campo_Tiro.objects.filter(nombre__icontains=nombre)

    return render(request, 'campos.html', {'campos': campos})



def registro_usuario(request):
    if request.method == 'GET':
        return render(request, 'registro.html')
    else:
        username = request.POST.get('username')
        email = request.POST.get('email')
        birthdate = request.POST.get('birthdate')
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
                return render(request, 'registro.html', {"errores":errors, "username": username, "email":email, 'birthdate':birthdate})
        else:
            user = Usuario.objects.create(username=username, password=make_password(password), email=email, birthdate=birthdate)
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

def acceso_denegado(request):
    return render(request, 'acceso_denegado.html')

def ver_carrito(request):
    carrito = Carrito()

    if "carrito" in request.session:
        carrito = carrito.from_dict(request.session["carrito"])

    return render(request, "carrito_producto.html", {"carrito": carrito})

def comprar_producto(request, id):
    producto = Producto.objects.get(id=id)
    carrito = Carrito()
    list_producto = Producto.objects.all()

    #Compruebo que en sesion esta la variable "carrito"
    if "carrito" in request.session:
        carrito = carrito.from_dict(request.session["carrito"])

    #Compruebo que el producto esta en el carrito
    if carrito.comprobar_producto_en_carrito(id):
        producto_carrito = carrito.obtener_producto(id)
        carrito.actualizar_producto(id, producto_carrito.cantidad + 1)
    else:
        producto_carrito = ProductoCarrito(producto.id, producto.nombre,producto.precio,1,producto.foto)
        carrito.agregar_producto(producto_carrito)

    request.session["carrito"] = carrito.to_dict()

    return render(request, 'productos.html',{'productos': list_producto})

def vaciar_carro(request):
    carrito = Carrito()

    if "carrito" in request.session:
        carrito = carrito.vaciar_carrito()
        del request.session["carrito"]

    return render(request,"carrito_producto.html", {"carrito":carrito})

def eliminar_producto_carro(request,id):
    carrito = Carrito()

    if "carrito" in request.session:
        carrito = carrito.from_dict(request.session["carrito"])

    if carrito.comprobar_producto_en_carrito(id):
        carrito.eliminar_producto(id)

    request.session["carrito"] = carrito.to_dict()

    return render(request, 'carrito_producto.html', {"carrito": carrito})

def sumar_producto_carro(request,id):
    carrito = Carrito()

    if "carrito" in request.session:
        carrito = carrito.from_dict(request.session["carrito"])

    if carrito.comprobar_producto_en_carrito(id):
        producto_carrito = carrito.obtener_producto(id)
        if producto_carrito.cantidad >= 1:
            carrito.actualizar_producto(id, producto_carrito.cantidad + 1)

    request.session["carrito"] = carrito.to_dict()

    return render(request, 'carrito_producto.html', {"carrito": carrito})

def restar_producto_carro(request,id):
    carrito = Carrito()

    if "carrito" in request.session:
        carrito = carrito.from_dict(request.session["carrito"])

    if carrito.comprobar_producto_en_carrito(id):
        producto_carrito = carrito.obtener_producto(id)
        if producto_carrito.cantidad > 1:
            carrito.actualizar_producto(id, producto_carrito.cantidad - 1)


    request.session["carrito"] = carrito.to_dict()

    return render(request, 'carrito_producto.html', {"carrito":carrito})

def hacer_pedido(request):
    carrito = Carrito()
    list_producto = Producto.objects.all()
    if "carrito" in request.session:
        carrito = carrito.from_dict(request.session["carrito"])

    pedido = Pedido.objects.create(
        identificador=''.join(random.choices(string.digits, k=8)),
        usuario= request.user
    )

    for itemsCarrito in carrito.productos:
        items = ItemsPedido.objects.create(
            nombre= itemsCarrito.nombre,
            cantidad= itemsCarrito.cantidad,
            precio= itemsCarrito.precio,
            total= itemsCarrito.precio * itemsCarrito.cantidad,
            pedido= pedido
        )
        ItemsPedido.save(items)

    return vaciar_carro(request)

def listar_pedidos(request):
    usuario = request.user
    lista_pedidos = []

    if usuario != None:
        lista_pedidos = Pedido.objects.filter(usuario=usuario)
    return render(request, 'pedidos_producto.html', {'pedidos': lista_pedidos})

def eliminar_pedido(request,id):
    pedido = Pedido.objects.get(id=id)
    pedido.delete()
    return listar_pedidos(request)

def listar_productos_pedido(request,id):
    pedido = Pedido.objects.get(id=id)
    lista_producto_pedido = ItemsPedido.objects.filter(pedido=pedido)
    return render(request, 'items_pedido.html', {'producto_pedidos': lista_producto_pedido})



def mostrar_eventos(request):
    lista_eventos = Evento.objects.all()
    return render(request, 'eventos.html', {'eventos':lista_eventos})

def crear_evento(request):
    if request.method == 'GET':
        campos = Campo_Tiro.objects.all()
        return render(request, 'crear_evento.html', {'campos':campos})
    else:
        nuevo_evento = Evento()
        nuevo_evento.nombre = request.POST.get("evento_nombre")
        nuevo_evento.imagen_evento = request.POST.get("evento_imagen")
        nuevo_evento.precio = float(request.POST.get("evento_precio"))
        nuevo_evento.fecha = request.POST.get("evento_fecha")
        nuevo_evento.aforo = request.POST.get("evento_aforo")

        nuevo_evento.save()

        campos = request.POST.getlist("evento_campo")

        for c in campos:
            campo = Campo_Tiro.objects.get(id=c)
            nuevo_evento.campo_tiro.add(campo)


        return redirect("mostrar_eventos")



def editar_evento(request, id):
    if request.method == 'GET':
        eventos = Evento.objects.get(id=id)
        campos = Campo_Tiro.objects.all()
        id_campo = eventos.campo_tiro.values_list('id', flat=True)
        return render(request, 'crear_evento.html', {'eventos':eventos, 'campos':campos, 'id_campo':id_campo})
    else:
        evento = Evento()

        evento.id = id
        evento.nombre = request.POST.get('evento_nombre')
        evento.fecha = request.POST.get('evento_fecha')
        evento.precio = float(request.POST.get('evento_precio'))
        evento.imagen_evento = request.POST.get('evento_imagen')
        evento.descripcion = request.POST.get('evento_descripcion')
        evento.aforo = request.POST.get("evento_aforo")
        evento.save()
        evento.campo_tiro.clear()
        evento.campo_tiro.set
        return redirect('/lista_eventos')

def eliminar_evento(request, id):
    evento = Evento.objects.get(id=id)
    if evento is not None:
        Evento.delete(evento)
        return redirect('/lista_eventos')


def evento_detalles(request, id):
    evento = Evento.objects.get(id=id)
    return render(request, 'evento_detalles.html', {'evento':evento})



def ver_panel_administracion(request):
    return render(request, 'panel_administrador.html')

def ir_a_perfil_usuario(request):
   return render(request, 'perfil_usuario.html')

def reservar_evento(request, id):
    if request.method =='GET':
        evento = Evento.objects.get(id=id)
        tramos = Tramo_reserva.values
        campos = Campo_Tiro.objects.all()
        precio_evento = evento.precio
        fecha_evento = evento.fecha
        return render(request, 'reservar_evento.html', {'tramos':tramos, 'campos':campos, 'precio_evento':precio_evento, 'fecha_evento':fecha_evento})
    else:
        # user = request.user
        # birthdate = date(user.birthdate)
        # fecha_nacimiento =
        # fecha = date.today()
        # edad =fecha.year - birthdate.year
        #
        # if edad <18:
        #     messages.success(request, "Debes ser mayor de 18 para poder inscribirte")
        #     return redirect(reverse('reservar_evento', args=[id]))
        reserva_evento = Reserva()
        reserva_evento.tramo_horario = int(Tramo_reserva.choices[int(request.POST.get("tramo_reserva")) - 1][0])
        reserva_evento.evento_id = id
        reserva_evento.precio_reserva = request.POST.get('precio_reserva')
        reserva_evento.jugador = request.user
        reserva_evento.fecha = request.POST.get('fecha_reserva')
        reserva_evento.num_jugadores= int(request.POST.get('num_jugadores'))

        if reserva_evento.tramo_horario is None or reserva_evento.num_jugadores is None:
            messages.success(request, "Debes indicar el tramo horario y el número de jugadores")
            return redirect(reverse('reservar_evento', args=[id]))

        reserva_num_personas = reserva_evento.num_jugadores
        evento = Evento.objects.get(id=id)
        aforo = evento.aforo
        if reserva_num_personas > aforo:
            messages.success(request, "El número de jugadores excede el aforo")
            return redirect(reverse('reservar_evento', args=[id]))

        if Reserva.objects.filter(tramo_horario=reserva_evento.tramo_horario, fecha=reserva_evento.fecha):
            messages.success(request, "El tramo horario ya está cogido para esa fecha")
            return redirect(reverse('reservar_evento', args=[id]))

        reserva_evento.save()
        return redirect('/')

def reservar_campo(request, id):
    if request.method == 'GET':
        campo = Campo_Tiro.objects.get(id=id)
        tramos = Tramo_reserva.values
        return render(request, 'reservar_campo.html', {'campo': campo, 'tramos': tramos})
    else:
        reserva_campo = Reserva()
        reserva_campo.tramo_horario = int(Tramo_reserva.choices[int(request.POST.get("tramo_reserva")) - 1][0])
        reserva_campo.evento_id = id
        reserva_campo.precio_reserva = request.POST.get('precio_reserva')
        reserva_campo.jugador = request.user
        reserva_campo.fecha = request.POST.get('fecha_reserva')
        reserva_campo.num_jugadores = request.POST.get('num_jugadores')

        reserva_campo.save()

        return redirect('/inicio')






