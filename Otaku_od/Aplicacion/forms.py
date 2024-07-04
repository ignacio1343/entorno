from django import forms
from .models import Producto
from .models import TipoProducto
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ValidationError
import re
from django import forms

class TipoProductoForm(forms.ModelForm):
    
    class Meta:
        model = TipoProducto
        fields = '__all__'

class ProductoForm(forms.ModelForm):
    
    nombre = forms.CharField(min_length=3, max_length=50)
    stock = forms.IntegerField(min_value=1)
    valor = forms.IntegerField(min_value=1)
    
    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        existe = Producto.objects.filter(nombre__iexact=nombre).exists()  # Corregir el uso de exists()
        if existe:
            raise forms.ValidationError('El nombre debe de ser unico')
        return nombre
    
    class Meta:
        model = Producto
        fields = '__all__'


class ModificarPersonaForm(forms.ModelForm):
    
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email']
        
class CustomUserCreationForm(UserCreationForm):
    
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email','password1','password2']
        
    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if not re.match(r'^[a-zA-ZáéíóúüñÁÉÍÓÚÜÑ ]+$', first_name):
            raise forms.ValidationError("El nombre solo puede contener letras y espacios.")
        return first_name
    
    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if not re.match(r'^[a-zA-ZáéíóúüñÁÉÍÓÚÜÑ ]+$', last_name):
            raise forms.ValidationError("El apellido solo puede contener letras y espacios.")
        return last_name

