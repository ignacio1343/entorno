from django import forms
from .models import Producto
from .models import TipoProducto
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ValidationError
from .models import *
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
    
    class Meta:
        model = Producto
        fields = '__all__'
    
class ModificarProductoForm(forms.ModelForm):
    
    nombre = forms.CharField(min_length=3, max_length=50)
    stock = forms.IntegerField(min_value=1)
    valor = forms.IntegerField(min_value=1)
    
    class Meta:
        model = Producto
        fields = ['nombre', 'stock', 'valor']

class ModificarPedidoForm(forms.ModelForm):
    
    class Meta:
        model = Pedido
        fields = ['estado']

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
    

class AdminCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirm']

    def clean_password_confirm(self):
        password = self.cleaned_data.get("password")
        password_confirm = self.cleaned_data.get("password_confirm")
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Las contraseñas no coinciden")
        return password_confirm

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        user.is_staff = True
        if commit:
            user.save()
        return user

