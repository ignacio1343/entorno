from django.db import models
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .enumeraciones import *

class TipoProducto(models.Model):
    nombre = models.CharField(max_length=50, null=False)

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    nombre = models.CharField(max_length=50, null=False)
    tipo = models.ForeignKey(TipoProducto, on_delete=models.PROTECT, null=False)
    stock = models.IntegerField(null=False)
    valor = models.IntegerField(null=False)
    imagen = models.ImageField(upload_to="Aplicacion/media/productos", null=True)

    def __str__(self):
        return f"Nombre:{self.nombre} Tipo: {self.tipo} Stock: {self.stock} Valor: {self.valor}"

class Carrito(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    session_key = models.CharField(max_length=40, null=True, blank=True)

    def __str__(self):
        return f'Carrito de {self.usuario if self.usuario else self.session_key}'

class ItemCarrito(models.Model):
    carrito = models.ForeignKey(Carrito, related_name='items', on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.cantidad} x {self.producto.nombre}'

class Pedido(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    fecha = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    estado =models.CharField(max_length=50, choices= sorted(ESTADO, key=lambda x: x[1]),default="Pagado")

    def calcular_total(self): 
        total = sum(item.producto.valor * item.cantidad for item in self.items.all())
        self.total = total
        self.save()
        return total

    def obtener_productos(self):
        return [f'{item.cantidad} x {item.producto.nombre}' for item in self.items.all()]

    @classmethod
    def calcular_total_todos_pedidos(cls):
        total = cls.objects.aggregate(total=models.Sum('total'))['total']
        return total if total is not None else 0.00

    def __str__(self):
        productos_str = ', '.join(self.obtener_productos())
        return f'Pedido de {self.usuario.username if self.usuario else "Usuario anónimo"} - Total: {self.total} - Productos: {productos_str}'

class PedidoProducto(models.Model):
    pedido = models.ForeignKey(Pedido, related_name='items', on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.cantidad} x {self.producto.nombre}'

@receiver(post_save, sender=Pedido)
def actualizar_total_pedido(sender, instance, created, **kwargs):
    if created:
        instance.calcular_total()

@receiver(post_save, sender=Carrito)
def crear_pedido(sender, instance, created, **kwargs):
    if created:
        pedido = Pedido.objects.create(usuario=instance.usuario)
        for item in instance.items.all():
            PedidoProducto.objects.create(pedido=pedido, producto=item.producto, cantidad=item.cantidad)
        pedido.calcular_total()
