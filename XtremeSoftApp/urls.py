from django.urls import path
from .views import *

urlpatterns = [
    path('', inicio, name='inicio'),
    path('nuevo_producto/', crear_producto, name='crear_producto'),
    path('lista_productos/', mostrar_productos, name='mostrar_productos'),
    path('productos/editar/<int:id>', editar_producto, name='editar_producto'),
    path('productos/eliminar/<int:id>', eliminar_producto, name='eliminar_producto'),
    path('productos/buscar/', buscar_productos, name="buscarproducto"),
    path('productos/comprar/<int:id>', comprar_producto, name="añadiralcarro"),

    path('lista_campos/', mostrar_campos, name='mostrar_campos'),

    path('nuevo_campo_de_tiro/', crear_campo, name='crear_campo_de_tiro'),
    path('nuevo_campo_de_tiro/editar/<int:id>', editar_campo, name='editar_campo_de_tiro'),
    path('nuevo_campo_de_tiro/eliminar/<int:id>', eliminar_campo, name='eliminar_campo_de_tiro'),
    path('nuevo_campo_de_tiro/buscar/', buscar_campos, name="buscarcampo"),

    path('empleado/nuevo/', crear_empleado, name='crear_empleado'),
    path('lista_empleados/', ver_empleados, name='ver_empleados'),
    path('empleados/eliminar/<int:id>', eliminar_empleado, name='eliminar_empleado'),
    path('empleados/editar/<int:id>', editar_empleado, name='editar_empleado'),
    path('empleado/usuario/<int:id>', crear_usuario_empleado, name='usuario_empleado'),

    path('usuario/registro/', registro_usuario, name='registro_usuario'),
    path('usuario/login', do_login, name='do_login'),
    path('logout/', do_logout, name='do_logout'),

    path('carrito/', ver_carrito, name="carrito"),
    path('carrito/vaciarcarro/', vaciar_carro, name="vaciarcarro"),
    path('carrito/eliminar/<int:id>', eliminar_producto_carro, name="eliminarproductocarro"),
    path('carrito/sumar/<int:id>', sumar_producto_carro, name="sumarcarro"),
    path('carrito/restar/<int:id>', restar_producto_carro, name="restarcarro"),
    path('carrito/hacerpedido/', hacer_pedido, name="hacerpedido"),

    path('mispedidos/', listar_pedidos, name="mispedidos"),
    path('mispedidos/eliminar/<int:id>', eliminar_pedido, name="mispedidos"),
    path('mispedidos/productos/<int:id>', listar_productos_pedido, name="misproductos"),

    path('acceso_denegado/', acceso_denegado, name='acceso_denegado'),
    path('acceso_denegado/', acceso_denegado, name='acceso_denegado'),

    path('lista_eventos/', mostrar_eventos, name='mostrar_eventos'),
    path('nuevo_evento/', crear_evento, name='crear_evento'),
    path('editar_evento/<int:id>', editar_evento, name='editar_evento'),
    path('eliminar_evento/<int:id>', eliminar_evento, name='eliminar_evento'),
    path('evento/detalle/<int:id>', evento_detalles, name='evento_detalles'),

    path('panel_administracion/', ver_panel_administracion, name="ver_panel_administracion"),

    path('perfil_usuario', ir_a_perfil_usuario, name="ir_a_perfil_usuario")



]
