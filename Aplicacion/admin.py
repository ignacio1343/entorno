from django.contrib import admin
from .models import *
from .forms import *

# Register your models here.

class ProductoAdmin(admin.ModelAdmin):
    list_display = ["nombre", "tipo", "stock", "valor"]
    list_editable = ["stock","valor"]
    search_fields = ["nombre"]
    list_filter = ["tipo", "valor"]
    list_per_page= 5
    form = ProductoForm

admin.site.register(Producto, ProductoAdmin)
admin.site.register(TipoProducto)
admin.site.register(Pedido)
admin.site.register(PedidoProducto)