from django.shortcuts import render, redirect, get_object_or_404
from .models import Producto
from .forms import ProductoForm
from django.contrib.auth.models import User
from .forms import CustomUserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login
from .models import *
from .forms import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404 
from rest_framework import viewsets
from .serializers import ProductoSerializer
from django.contrib.auth.decorators import login_required
from functools import wraps
from django.http import HttpResponseForbidden
# Create your views here.

class ProductoViewset(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    
    def get_queryset(self):
        productos = Producto.objects.all()
        
        nombre = self.request.GET.get('nombre')
        if nombre:
            productos = productos.filter(nombre__contains=nombre)
        return productos
    
def admin_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_staff:
            return redirect('index')
        return view_func(request, *args, **kwargs)
    return _wrapped_view


def index(request):
    productos = Producto.objects.all()
    data = {
        'productos': productos
    }
    return render(request, 'Otaku_ody/index.html', data)

def preguntas(request):
    return render(request, 'Otaku_ody/preguntas.html')

@login_required
def pedidos_user(request):
    return render(request, 'Otaku_ody/pedidos_user.html')

def t_productos(request):
    productos = Producto.objects.all()
    paginator = Paginator(productos, 8)  # Crear un objeto Paginator con tus productos

    page = request.GET.get('page')  # Obtener el número de página desde la URL
    try:
        productos_paginados = paginator.get_page(page)
    except PageNotAnInteger:
        # Si la página no es un entero, mostrar la primera página
        productos_paginados = paginator.get_page(1)
    except EmptyPage:
        # Si la página está fuera del rango (por ejemplo, 9999), mostrar la última página de resultados
        productos_paginados = paginator.get_page(paginator.num_pages)

    
    data = {
        'entity': productos_paginados,
        'paginator': paginator,
    }
    return render(request, 'Otaku_ody/t_productos.html', data)

def contacto(request):
    return render(request, 'Otaku_ody/contacto.html')

@admin_required
def administracion(request):
    return render(request, 'Otaku_ody/administracion.html')
@admin_required
def listaproducto(request):
    productos = Producto.objects.all()
    paginator = Paginator(productos, 4)  # Crear un objeto Paginator con tus productos

    page = request.GET.get('page')  # Obtener el número de página desde la URL
    try:
        productos_paginados = paginator.get_page(page)
    except PageNotAnInteger:
        # Si la página no es un entero, mostrar la primera página
        productos_paginados = paginator.get_page(1)
    except EmptyPage:
        # Si la página está fuera del rango (por ejemplo, 9999), mostrar la última página de resultados
        productos_paginados = paginator.get_page(paginator.num_pages)

    
    data = {
        'entity': productos_paginados,
        'paginator': paginator,
    }
    return render(request, 'Otaku_ody/listaproducto.html', data)
@admin_required
def agregarproducto(request):
    data = {
        'form': ProductoForm()
    }
    
    if request.method == 'POST':
        formulario = ProductoForm(data=request.POST, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request,'Producto Agregado')
            return redirect(to="listaproducto")
        else:
            data["mensaje"] = "Rellena bien todos los campos"
    
    return render(request, 'Otaku_ody/agregarproducto.html', data)
@admin_required
def modificarproducto(request, id):
    producto = get_object_or_404(Producto, id=id)
    
    data = {
        'form' : ModificarProductoForm(instance=producto)
    }
    
    if request.method == 'POST':
        formulario = ModificarProductoForm(data=request.POST, instance=producto, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request,'Producto Modificado')
            return redirect(to="listaproducto")
        data["form"] = formulario
    
    return render(request, 'Otaku_ody/modificarproducto.html', data)
@admin_required
def eliminarproducto(request, id):
    producto = get_object_or_404(Producto, id=id)
    producto.delete()
    messages.warning(request, 'Producto Eliminado')
    return redirect(to="listaproducto")
@admin_required
def usuarios(request):
    personas = User.objects.all()
    paginator = Paginator(personas, 4)  # Crear un objeto Paginator con tus productos

    page = request.GET.get('page')  # Obtener el número de página desde la URL
    try:
        usuarios_paginados = paginator.get_page(page)
    except PageNotAnInteger:
        # Si la página no es un entero, mostrar la primera página
        usuarios_paginados = paginator.get_page(1)
    except EmptyPage:
        # Si la página está fuera del rango (por ejemplo, 9999), mostrar la última página de resultados
        usuarios_paginados = paginator.get_page(paginator.num_pages)

    
    data = {
        'entity': usuarios_paginados,
        'paginator': paginator,
    }
    return render(request, 'Otaku_ody/usuarios.html', data)
@admin_required
def agregarusuario(request):
    data = {
        'form': CustomUserCreationForm()
    }
    
    if request.method == 'POST':
        formulario = CustomUserCreationForm(data=request.POST, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request,'Persona Agregada')
            return redirect(to="usuarios")
        else:
            data["mensaje"] = "Rellena bien todos los campos"
    
    return render(request, 'Otaku_ody/agregarusuario.html', data)
@admin_required
def modificarusuario(request, id):
    persona = get_object_or_404(User, id=id)
    
    data = {
        'form' : CustomUserCreationForm(instance=persona)
    }
    
    if request.method == 'POST':
        formulario = CustomUserCreationForm(data=request.POST, instance=persona, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request,'Persona Modificada')
            return redirect(to="usuarios")
        data["form"] = formulario
    
    return render(request, 'Otaku_ody/modificarusuario.html', data)
@admin_required
def eliminarusuario(request, id):
    persona = get_object_or_404(User, id=id)
    persona.delete()
    messages.warning(request, 'Persona Eliminada')
    return redirect(to="usuarios")
@admin_required
def tipoproducto(request):
    productos = TipoProducto.objects.all()
    data = {
        'productos': productos
    }
    return render(request, 'Otaku_ody/tipoproducto.html', data)
@admin_required
def agregartipoproducto(request):
    data = {
        'form': TipoProductoForm()
    }
    if request.method == 'POST':
        formulario = TipoProductoForm(data=request.POST, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request,'Tipo de producto agregado')
            return redirect(to="tipoproducto")
        else:
            data["mensaje"] = "Rellena bien todos los campos"
    
    return render(request, 'Otaku_ody/agregartipoproducto.html', data)
    
@admin_required
def modificartipoproducto(request, id):
    tipoproducto = get_object_or_404(TipoProducto, id=id)
    
    data = {
        'form' : TipoProductoForm(instance=tipoproducto)
    }
    
    if request.method == 'POST':
        formulario = TipoProductoForm(data=request.POST, instance=tipoproducto, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request,'Tipo de producto modificado')
            return redirect(to="tipoproducto")
        data["form"] = formulario
    
    return render(request, 'Otaku_ody/modificartipoproducto.html', data)
@admin_required
def eliminartipoproducto(request, id):
    tipoproducto = get_object_or_404(TipoProducto, id=id)
    tipoproducto.delete()
    messages.warning(request, 'Tipo de producto Eliminado')
    return redirect(to="tipoproducto")


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

@admin_required
def crearadmin(request):
    if request.method == 'POST':
        form = AdminCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')  # Redirigir a la página que desees después de crear el administrador
    else:
        form = AdminCreationForm()
    return render(request, 'Otaku_ody/crearadmin.html', {'form': form})

def test(request):
    productos = Producto.objects.all()
    data = {
        'productos': productos
    }
    return render(request, 'Otaku_ody/test.html', data)

def carrito(request):
    return render(request, 'Otaku_ody/carrito.html')

def estadisticas(request):
    return render(request, 'Otaku_ody/estadisticas.html')

def pedidos(request):
    return render(request, 'Otaku_ody/pedidos.html')
    
def listapedido(request):
    pedidos = PedidoProducto.objects.all()
    data = {
        'pedidos': pedidos
    }
    return render(request, 'Otaku_ody/pedidos.html', data)
