from django.contrib.auth.models import UserManager
from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager

# Create your models here.

#Aqui vamos a crear clases como tablas de base de datos, todas ellas extienden models.model

class Rol(models.TextChoices):
    ADMIN = "ADMIN", "Administrador"
    CUSTOMER = "CUST", "Cliente"
    EMPLOYEE = "EMP", "Empleado"



class Usuario(AbstractBaseUser):
    email = models.EmailField(max_length=255,unique=True)
    username = models.CharField(unique=True, max_length=255)
    rol = models.CharField(max_length=15, choices=Rol.choices, default=Rol.CUSTOMER)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['mail', "rol"]
    def __str__(self):
        return self.username, self.email


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("El campo email es obligatorio")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("Error. El campo is_staff debe ser True")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Error. El campo is_superuser debe ser True")

        return self.create_user(email, password, **extra_fields)





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
    precio = models.FloatField()
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
    image = models.CharField(max_length=1000, default="")
    aforo = models.IntegerField(null= False)
    nombre = models.CharField(max_length=200)
    localizacion = models.CharField(max_length=300)

    def __str__(self):
        return self.nombre

class Empleado(models.Model):
    nombre = models.CharField(max_length=500)
    fecha_nacimiento = models.DateField(null=False)
    codigo = models.CharField(max_length=9)
    mail = models.CharField(max_length=500)
    image_url = models.CharField(max_length=900)
    usuario = models.ForeignKey(Usuario, null=True, on_delete=models.CASCADE)
    campos = models.ManyToManyField(Campo_Tiro, null=False)

    def __str__(self):
        return str(self.id) + " - " + self.nombre
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
    imagen_evento = models.CharField(max_length=900, default=True)
    campo_tiro = models.ManyToManyField(Campo_Tiro, null=False, blank=False)


    def __str__(self):
        return self.nombre, self.fecha
