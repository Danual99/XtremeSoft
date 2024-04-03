from django.db import models


# Create your models here.

#Aqui vamos a crear clases como tablas de base de datos, todas ellas extienden models.model


class Usuario(models.Model):
    email = models.EmailField(max_length=255,unique=True)
    username = models.CharField(unique=True, max_length=255, blank=False)
    password = models.CharField(max_length=255, blank=False)

    def __str__(self):
        return self.username, self.email


class Pedido(models.Model):
    id = models.AutoField(primary_key=True)
    num_pedido = models.IntegerField()
    fecha = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(Usuario, null=False, blank=False, on_delete=models.CASCADE)

    def __str__(self):
        return self.num_pedido, self.fecha

class Producto(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=250)
    descripcion = models.CharField(max_length=250)
    precio = models.IntegerField()
    foto = models.CharField(max_length=1000, default="")

    def __str__(self):
        return self.nombre, self.precio

class ItemsPedido(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=250)
    cantidad = models.IntegerField()
    precio = models.FloatField()
    total = models.FloatField()
    pedido = models.ForeignKey(Pedido, null=False, blank=False, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, null=False, blank=False, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre, self.total

class Campo_Tiro(models.Model):
    id = models.AutoField(primary_key=True)
    aforo = models.IntegerField(null= False)
    nombre = models.CharField(max_length=200)
    localizacion = models.CharField(max_length=300)

    def __str__(self):
        return self.nombre

class Tramo_reserva(models.TextChoices):
    T1 = 1
    T2 = 2
    T3 = 3

class Reserva(models.Model):
    id = models.AutoField(primary_key=True)
    tramo_horario = models.IntegerField(null=False, choices=Tramo_reserva.choices)
    fecha = models.DateField(null=False)
    num_jugadores = models.IntegerField(null=False)
    precio_reserva = models.FloatField(null=False)
    campo_tiro = models.ForeignKey(Campo_Tiro, null=False, blank=False, on_delete=models.CASCADE)
    jugador = models.ForeignKey(Usuario, null=False, blank=False, on_delete=models.CASCADE)

    def __str__(self):
        return self.fecha, self.tramo_horario, self.num_jugadores

class Evento(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=300)
    fecha = models.DateField(null=False)
    precio = models.FloatField(null=False)
    campo_tiro = models.ForeignKey(Campo_Tiro, null=False, blank=False, on_delete=models.CASCADE)
    jugador = models.ForeignKey(Usuario, null=False, blank=False, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre, self.fecha
