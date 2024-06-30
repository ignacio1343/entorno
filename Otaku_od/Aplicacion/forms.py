from django import forms
from .models import Producto

class ProductoForm(forms.ModelForm):
    
    nombre= forms.CharField(widget=forms.TextInput(attrs={"class":"form-control"}))
    
    class Meta:
        model = Producto
        fields = '__all__'
