from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets
from functools import wraps
from django.core.exceptions import ValidationError


from .models import Producto, Carrito, ItemCarrito, TipoProducto
from .forms import ProductoForm, CustomUserCreationForm, ModificarProductoForm, TipoProductoForm, AdminCreationForm
from .serializers import ProductoSerializer
from .models import Carrito, Producto, ItemCarrito, Pedido, PedidoProducto
from .models import *
from .forms import *

# Decorador para restringir vistas a administradores
def admin_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_staff:
            return redirect('index')
        return view_func(request, *args, **kwargs)
    return _wrapped_view

# Vista para el índice
def index(request):
    productos = Producto.objects.all()
    return render(request, 'Otaku_ody/index.html', {'productos': productos})

# Vista para preguntas frecuentes
def preguntas(request):
    return render(request, 'Otaku_ody/preguntas.html')

# Vista para los pedidos del usuario
@login_required
def pedidos_user(request):
    return render(request, 'Otaku_ody/pedidos_user.html')

# Vista para listar productos con paginación
def t_productos(request):
    productos = Producto.objects.all()
    paginator = Paginator(productos, 8)

    page = request.GET.get('page')
    try:
        productos_paginados = paginator.get_page(page)
    except PageNotAnInteger:
        productos_paginados = paginator.get_page(1)
    except EmptyPage:
        productos_paginados = paginator.get_page(paginator.num_pages)

    return render(request, 'Otaku_ody/t_productos.html', {'entity': productos_paginados, 'paginator': paginator})

# Vista para la página de contacto
def contacto(request):
    return render(request, 'Otaku_ody/contacto.html')

# Vistas para administración
@admin_required
def administracion(request):
    return render(request, 'Otaku_ody/administracion.html')

@admin_required
def listaproducto(request):
    productos = Producto.objects.all()
    paginator = Paginator(productos, 4)

    page = request.GET.get('page')
    try:
        productos_paginados = paginator.get_page(page)
    except PageNotAnInteger:
        productos_paginados = paginator.get_page(1)
    except EmptyPage:
        productos_paginados = paginator.get_page(paginator.num_pages)

    return render(request, 'Otaku_ody/listaproducto.html', {'entity': productos_paginados, 'paginator': paginator})

@admin_required
def agregarproducto(request):
    form = ProductoForm()
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto Agregado')
            return redirect('listaproducto')
    return render(request, 'Otaku_ody/agregarproducto.html', {'form': form})

@admin_required
def modificarproducto(request, id):
    producto = get_object_or_404(Producto, id=id)
    form = ModificarProductoForm(instance=producto)
    if request.method == 'POST':
        form = ModificarProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto Modificado')
            return redirect('listaproducto')
    return render(request, 'Otaku_ody/modificarproducto.html', {'form': form})

@admin_required
def eliminarproducto(request, id):
    producto = get_object_or_404(Producto, id=id)
    producto.delete()
    messages.warning(request, 'Producto Eliminado')
    return redirect('listaproducto')

@admin_required
def usuarios(request):
    personas = User.objects.all()
    paginator = Paginator(personas, 4)

    page = request.GET.get('page')
    try:
        usuarios_paginados = paginator.get_page(page)
    except PageNotAnInteger:
        usuarios_paginados = paginator.get_page(1)
    except EmptyPage:
        usuarios_paginados = paginator.get_page(paginator.num_pages)

    return render(request, 'Otaku_ody/usuarios.html', {'entity': usuarios_paginados, 'paginator': paginator})

@admin_required
def agregarusuario(request):
    form = CustomUserCreationForm()
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Persona Agregada')
            return redirect('usuarios')
    return render(request, 'Otaku_ody/agregarusuario.html', {'form': form})

@admin_required
def modificarusuario(request, id):
    persona = get_object_or_404(User, id=id)
    form = CustomUserCreationForm(instance=persona)
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES, instance=persona)
        if form.is_valid():
            form.save()
            messages.success(request, 'Persona Modificada')
            return redirect('usuarios')
    return render(request, 'Otaku_ody/modificarusuario.html', {'form': form})

@admin_required
def eliminarusuario(request, id):
    persona = get_object_or_404(User, id=id)
    persona.delete()
    messages.warning(request, 'Persona Eliminada')
    return redirect('usuarios')

@admin_required
def pedidos(request):
    pedidos = Pedido.objects.all()
    for pedido in pedidos:
        pedido.calcular_total()  # Calcula y guarda el total
        pedido.productos = pedido.obtener_productos()
    paginator = Paginator(pedidos, 4)

    page = request.GET.get('page')
    try:
        pedidos_paginados = paginator.get_page(page)
    except PageNotAnInteger:
        pedidos_paginados = paginator.get_page(1)
    except EmptyPage:
        pedidos_paginados = paginator.get_page(paginator.num_pages)

    return render(request, 'Otaku_ody/pedidos.html', {'pedidos': pedidos, 'entity': pedidos_paginados, 'paginator': paginator})

@admin_required
def modificarpedido(request, id):
    pedidos = get_object_or_404(Pedido, id=id)
    form = ModificarPedidoForm(instance=pedidos)
    if request.method == 'POST':
        form = ModificarPedidoForm(request.POST, request.FILES, instance=pedidos)
        if form.is_valid():
            form.save()
            messages.success(request, 'Pedido agregado')
            return redirect('pedidos')
    return render(request, 'Otaku_ody/modificarpedido.html', {'form': form})

@admin_required
def tipoproducto(request):
    productos = TipoProducto.objects.all()
    return render(request, 'Otaku_ody/tipoproducto.html', {'productos': productos})

@admin_required
def agregartipoproducto(request):
    form = TipoProductoForm()
    if request.method == 'POST':
        form = TipoProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tipo de producto agregado')
            return redirect('tipoproducto')
    return render(request, 'Otaku_ody/agregartipoproducto.html', {'form': form})

@admin_required
def modificartipoproducto(request, id):
    tipoproducto = get_object_or_404(TipoProducto, id=id)
    form = TipoProductoForm(instance=tipoproducto)
    if request.method == 'POST':
        form = TipoProductoForm(request.POST, request.FILES, instance=tipoproducto)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tipo de producto modificado')
            return redirect('tipoproducto')
    return render(request, 'Otaku_ody/modificartipoproducto.html', {'form': form})

@admin_required
def eliminartipoproducto(request, id):
    tipoproducto = get_object_or_404(TipoProducto, id=id)
    tipoproducto.delete()
    messages.warning(request, 'Tipo de producto Eliminado')
    return redirect('tipoproducto')

# Vistas para autenticación
def login_view(request):
    return render(request, 'registration/login.html')

def registro(request):
    form = CustomUserCreationForm()
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            user = authenticate(username=form.cleaned_data["username"], password=form.cleaned_data["password1"])
            login(request, user)
            messages.success(request, "Te has registrado correctamente")
            return redirect('index')
    return render(request, 'registration/registro.html', {'form': form})

@admin_required
def crearadmin(request):
    form = AdminCreationForm()
    if request.method == 'POST':
        form = AdminCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    return render(request, 'Otaku_ody/crearadmin.html', {'form': form})

# Vista para estadísticas
def estadisticas(request):
    return render(request, 'Otaku_ody/estadisticas.html')

# Vista de prueba
def test(request):
    productos = Producto.objects.all()
    return render(request, 'Otaku_ody/test.html', {'productos': productos})

@login_required
def carrito(request):
    return render(request, 'Otaku_ody/carrito.html')

def get_or_create_cart(request):
    if request.user.is_authenticated:
        carrito, created = Carrito.objects.get_or_create(usuario=request.user)
    else:
        session_key = request.session.session_key or request.session.create()
        carrito, created = Carrito.objects.get_or_create(session_key=session_key)
    return carrito

@login_required
def agregar_al_carrito(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    carrito = get_or_create_cart(request)
    item, item_created = ItemCarrito.objects.get_or_create(carrito=carrito, producto=producto)
    if not item_created:
        item.cantidad += 1
        item.save()
    return redirect('ver_carrito')

@login_required
def ver_carrito(request):
    carrito = get_or_create_cart(request)
    items = carrito.items.all()
    total = sum(item.producto.valor * item.cantidad for item in items)
    return render(request, 'Otaku_ody/carrito.html', {'items': items, 'total': total})

@login_required
def eliminar_del_carrito(request, item_id):
    item = get_object_or_404(ItemCarrito, id=item_id)
    item.delete()
    return redirect('ver_carrito')

@login_required
def crear_pedido(request):
    carrito = get_or_create_cart(request)
    pedido = Pedido.objects.create(usuario=request.user)
    
    # Verificación y actualización del stock
    for item in carrito.items.all():
        if item.producto.stock < item.cantidad:
            raise ValidationError(f'No hay suficiente stock para el producto {item.producto.nombre}')
        item.producto.stock -= item.cantidad
        item.producto.save()
        PedidoProducto.objects.create(pedido=pedido, producto=item.producto, cantidad=item.cantidad)
    
    pedido.calcular_total()
    pedido.save()
    carrito.delete()  # Limpiar el carrito después de crear el pedido
    return redirect('ver_pedido', pedido_id=pedido.id)

@login_required
def ver_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    items = pedido.items.all()
    return render(request, 'Otaku_ody/pedido.html', {'pedido': pedido, 'items': items})

# Viewset para productos
class ProductoViewset(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

    def get_queryset(self):
        productos = Producto.objects.all()
        nombre = self.request.GET.get('nombre')
        if nombre:
            productos = productos.filter(nombre__contains=nombre)
        return productos
