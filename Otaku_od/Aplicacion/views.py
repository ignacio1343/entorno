from django.shortcuts import render, redirect, get_object_or_404
from .models import Producto
from .forms import ProductoForm
from .models import Persona
from .forms import PersonaForm
from .forms import ModificarPersonaForm, CustomUserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login

# Create your views here.

def index(request):
    productos = Producto.objects.all()
    data = {
        'productos': productos
    }
    return render(request, 'Otaku_ody/index.html', data)

def preguntas(request):
    return render(request, 'Otaku_ody/preguntas.html')

def v_itachi(request):
    return render(request, 'Otaku_ody/v_itachi.html')

def v_zenitsu(request):
    return render(request, 'Otaku_ody/v_zenitsu.html')

def pedidos_user(request):
    return render(request, 'Otaku_ody/pedidos_user.html')

def t_productos(request):
    productos = Producto.objects.all()
    data = {
        'productos': productos
    }
    return render(request, 'Otaku_ody/t_productos.html', data)

def contacto(request):
    return render(request, 'Otaku_ody/contacto.html')

def v_asuka(request):
    return render(request, 'Otaku_ody/v_asuka.html')

def v_goku(request):
    return render(request, 'Otaku_ody/v_goku.html')

def administracion(request):
    return render(request, 'Otaku_ody/administracion.html')

def listaproducto(request):
    productos = Producto.objects.all()
    data = {
        'productos': productos
    }
    return render(request, 'Otaku_ody/listaproducto.html', data)

def agregarproducto(request):
    data = {
        'form': ProductoForm()
    }
    
    if request.method == 'POST':
        formulario = ProductoForm(data=request.POST, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            data["mensaje"] = "Producto agregado"
            return redirect(to="listaproducto")
        else:
            data["mensaje"] = "Rellena bien todos los campos"
    
    return render(request, 'Otaku_ody/agregarproducto.html', data)

def modificarproducto(request, id):
    producto = get_object_or_404(Producto, id=id)
    
    data = {
        'form' : ProductoForm(instance=producto)
    }
    
    if request.method == 'POST':
        formulario = ProductoForm(data=request.POST, instance=producto, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            return redirect(to="listaproducto")
        data["form"] = formulario
    
    return render(request, 'Otaku_ody/modificarproducto.html', data)

def eliminarproducto(request, id):
    producto = get_object_or_404(Producto, id=id)
    producto.delete()
    return redirect(to="listaproducto")

def usuarios(request):
    personas = Persona.objects.all()
    data = {
        'personas': personas
    }
    return render(request, 'Otaku_ody/usuarios.html', data)

def agregarusuario(request):
    data = {
        'form': PersonaForm()
    }
    
    if request.method == 'POST':
        formulario = PersonaForm(data=request.POST, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            data["mensaje"] = "Persona agregado"
            return redirect(to="usuarios")
        else:
            data["mensaje"] = "Rellena bien todos los campos"
    
    return render(request, 'Otaku_ody/agregarusuario.html', data)

def modificarusuario(request, id):
    persona = get_object_or_404(Persona, rut=id)
    
    data = {
        'form' : ModificarPersonaForm(instance=persona)
    }
    
    if request.method == 'POST':
        formulario = ModificarPersonaForm(data=request.POST, instance=persona, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.warning(request,'Persona Modificada')
            return redirect(to="usuarios")
        data["form"] = formulario
    
    return render(request, 'Otaku_ody/modificarusuario.html', data)

def eliminarusuario(request, id):
    persona = get_object_or_404(Persona, rut=id)
    persona.delete()
    return redirect(to="usuarios")

def login(request, user):
    return render(request, 'registration/login.html')

def registro(request):
    data = {
        'form' : CustomUserCreationForm()
    }
    
    if request.method == 'POST':
        formulario = CustomUserCreationForm(data=request.POST)
        if formulario.is_valid():
            formulario.save()
            user=authenticate(username=formulario.cleaned_data["username"], password=formulario.cleaned_data["password1"])
            login(request, user)
            messages.success(request, "Te has registrado correctamente")
            return redirect(to="index")
        data["form"] = formulario
    
    return render(request, 'registration/registro.html', data)

def test(request):
    productos = Producto.objects.all()
    data = {
        'productos': productos
    }
    return render(request, 'Otaku_ody/test.html', data)