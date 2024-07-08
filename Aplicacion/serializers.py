from .models import *
from rest_framework import serializers


class TipoProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoProducto
        fields = '__all__'

class ProductoSerializer(serializers.ModelSerializer):
    nombretipo = serializers.CharField(read_only=True, source="tipo.nombre")
    tipoproducto = TipoProductoSerializer(read_only=True)
    tipoproducto_id = serializers.PrimaryKeyRelatedField(queryset=TipoProducto.objects.all(), source="tipo")
    nombre = serializers.CharField(required=True, min_length=3)
    
    def validate_nombre(self, value):
        existe = Producto.objects.filter(nombre__iexact=value).exists()
        
        if existe:
            raise serializers.ValidationError("Este producto ya existe")
        
        return value
    
    class Meta:
        model = Producto
        fields = '__all__'