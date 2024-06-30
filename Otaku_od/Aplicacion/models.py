from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

# Create your models here.

class Region(models.Model):
    nombre= models.CharField(max_length=50,null=False)

    def __str__(self):
        return self.nombre

class Comuna(models.Model):
    nombre= models.CharField(max_length=50,null=False)
    region = models.ForeignKey(Region, on_delete=models.PROTECT,null=False)

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
        return self.nombre
    