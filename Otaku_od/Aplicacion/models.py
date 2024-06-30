from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from .enumeraciones import *
from django.contrib.auth.models import User

# Create your models here.
class Comuna(models.Model):
    nombre= models.CharField(max_length=50,null=False)
    region = models.CharField(max_length=50,null=False, choices= sorted(REGIONES_CHILE, key=lambda x: x[1]),default="Pagado")

    def __str__(self):
        return f"Comuna:{self.nombre} Region: {self.region}"

class Persona(models.Model):
    rut= models.CharField(max_length=10,primary_key=True, null=False, error_messages='Coloca algo valido')
    nombre= models.CharField(max_length=50,null=False, error_messages='Coloca algo valido')
    apellido= models.CharField(max_length=50, null=False, error_messages='Coloca algo valido')
    correo= models.EmailField(null=False, error_messages='Coloca algo valido')
    comuna= models.ForeignKey(Comuna, on_delete=models.PROTECT,null=False)

    
    def __str__(self):
        return f"RUT:{self.rut} NOMBRE: {self.nombre} {self.apellido}"

class TipoProducto(models.Model):
    nombre= models.CharField(max_length=50,null=False, error_messages='Coloca algo valido')
    
    def __str__(self):
        return self.nombre

class Producto(models.Model):
    nombre= models.CharField(max_length=50,null=False, error_messages='Coloca algo valido')
    tipo= models.ForeignKey(TipoProducto, on_delete=models.PROTECT,null=False)
    stock= models.IntegerField(null=False)
    valor= models.IntegerField(null=False)
    imagen = models.ImageField(upload_to="Aplicacion/media/productos", null=True)
    
    def __str__(self):
        return f"Nombre:{self.nombre} Tipo: {self.tipo} Stock{self.stock} Valor{self.valor}"
    
class Pedido(models.Model):
    comprador = models.ForeignKey(Persona, on_delete=models.PROTECT, null=False)
    productos = models.ManyToManyField(Producto, through='PedidoProducto')

    @property
    def total(self):
        return sum(item.total for item in self.pedidoproducto_set.all())

    def __str__(self):
        return f"Comprador: {self.comprador} Total: {self.total}"

class PedidoProducto(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT)
    cantidad = models.IntegerField(null=False)
    estado=models.CharField(max_length=50, choices= sorted(ESTADO, key=lambda x: x[1]),default="Pagado")

    @property
    def valor(self):
        return self.producto.valor

    @property
    def total(self):
        return self.cantidad * self.valor

    def __str__(self):
        return f"Producto: {self.producto} Cantidad: {self.cantidad} Total: {self.total}"