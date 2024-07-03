from django import forms
from .models import Producto
from .models import TipoProducto
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class TipoProductoForm(forms.ModelForm):
    
    class Meta:
        model = TipoProducto
        fields = '__all__'

class ProductoForm(forms.ModelForm):
    
    nombre= forms.CharField(widget=forms.TextInput(attrs={"class":"form-control"}))
    
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