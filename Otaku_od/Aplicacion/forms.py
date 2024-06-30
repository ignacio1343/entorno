from django import forms
from .models import Producto, Persona

class ProductoForm(forms.ModelForm):
    
    nombre= forms.CharField(widget=forms.TextInput(attrs={"class":"form-control"}))
    
    class Meta:
        model = Producto
        fields = '__all__'


class PersonaForm(forms.ModelForm):
    
    class Meta:
        model = Persona
        fields = '__all__'

class ModificarPersonaForm(forms.ModelForm):
    
    class Meta:
        model = Persona
        fields = ['nombre','apellido','correo','comuna']