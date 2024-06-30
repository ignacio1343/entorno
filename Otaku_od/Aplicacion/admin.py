from django.contrib import admin
from .models import Region, Comuna, Persona, Producto, TipoProducto

# Register your models here.

class ProductoAdmin(admin.ModelAdmin):
    list_display = ["nombre", "tipo", "stock", "valor"]
    list_editable = ["stock","valor"]
    search_fields = ["nombre"]
    list_filter = ["tipo", "valor"]
    list_per_page= 5

admin.site.register(Region)
admin.site.register(Comuna)
admin.site.register(Persona)
admin.site.register(Producto, ProductoAdmin)
admin.site.register(TipoProducto)