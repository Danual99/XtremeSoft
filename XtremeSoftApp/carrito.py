
class ProductoCarrito():
    def __init__(self, id ,nombre ,precio ,cantidad ,foto):
        self.id = id
        self.nombre = nombre
        self.precio = precio
        self.cantidad = cantidad
        self.foto = foto

class Carrito():
    def __init__(self):
        self.productos = []


    def agregar_producto(self, producto):
        self.productos.append(producto)


    def actualizar_producto(self, id_producto, cantidad):
        for producto in self.productos:
            if producto.id == id_producto:
                producto.cantidad = cantidad

    def vaciar_carrito(self):
        self.productos = []

    def comprobar_producto_en_carrito(self, id):
        for producto in self.productos:
            if producto.id == id:
                return True
        return False

    def obtener_producto(self, id):
        for producto in self.productos:
            if producto.id == id:
                return producto
        return None

    def eliminar_producto(self,id):
        for producto in self.productos:
            if producto.id == id:
                self.productos.remove(producto)


    def to_dict(self):
        productos = [p.__dict__ for p in self.productos]
        return {"productos": productos}

    def from_dict(self, dict):
        carrito = self
        for p in dict["productos"]:
            producto = ProductoCarrito(p["id"], p["nombre"], p["precio"], p["cantidad"], p["foto"])
            carrito.agregar_producto(producto)
        return carrito

    def calcular_total(self):
        total = 0.0
        for producto in self.productos:
            total += producto.cantidad * producto.precio
        return total
