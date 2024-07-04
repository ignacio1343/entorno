from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from .enumeraciones import *
from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

# Create your models here.
    
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



class Carrito(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    session_key = models.CharField(max_length=40, null=True, blank=True)

    def str(self):
        return f'Carrito de {self.usuario if self.usuario else self.session_key}'

class ItemCarrito(models.Model):
    carrito = models.ForeignKey(Carrito, related_name='items', on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

    def str(self):
        return f'{self.cantidad} x {self.producto.nombre}'