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
    tipos = TipoProducto.objects.all()
    productos = Producto.objects.all()
    
    productos_por_tipo = {}
    for tipo in tipos:
        productos_por_tipo[tipo] = Producto.objects.filter(tipo=tipo)
    
    return render(request, 'Otaku_ody/index.html', {
        'productos': productos,
        'productos_por_tipo': productos_por_tipo,
    })
# Vista para preguntas frecuentes
def preguntas(request):
    return render(request, 'Otaku_ody/preguntas.html')

# Vista para los pedidos del usuario
@login_required
def pedidos_user(request):
    # Filtrar pedidos por el usuario actual
    pedidos = Pedido.objects.filter(usuario=request.user)

    for pedido in pedidos:
        pedido.calcular_total()  # Calcula y guarda el total
        pedido.productos = pedido.obtener_productos()

    paginator = Paginator(pedidos, 4)

    page = request.GET.get('page')
    try:
        pedidos_paginados = paginator.page(page)
    except PageNotAnInteger:
        pedidos_paginados = paginator.page(1)
    except EmptyPage:
        pedidos_paginados = paginator.page(paginator.num_pages)

    return render(request, 'Otaku_ody/pedidos_user.html', {'entity': pedidos_paginados, 'paginator': paginator})

# Vista para listar productos con paginación
def t_productos(request):
    tipos_productos = TipoProducto.objects.all()  # Obtener todos los tipos de productos
    tipo_seleccionado = request.GET.get('tipo')  # Obtener el tipo seleccionado del query string

    if tipo_seleccionado:
        productos = Producto.objects.filter(tipo__nombre=tipo_seleccionado)
    else:
        productos = Producto.objects.all()

    paginator = Paginator(productos, 8)
    page = request.GET.get('page')

    try:
        productos_paginados = paginator.page(page)
    except PageNotAnInteger:
        productos_paginados = paginator.page(1)
    except EmptyPage:
        productos_paginados = paginator.page(paginator.num_pages)

    return render(request, 'Otaku_ody/t_productos.html', {
        'entity': productos_paginados,
        'paginator': paginator,
        'tipos_productos': tipos_productos,
        'tipo_seleccionado': tipo_seleccionado
    })

# Vista para la página de contacto
def contacto(request):
    return render(request, 'Otaku_ody/contacto.html')

# Vistas para administración
@admin_required
def administracion(request):
    total_pedidos = Pedido.calcular_total_todos_pedidos()
    return render(request, 'Otaku_ody/administracion.html', {'total_pedidos': total_pedidos})

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
    if producto.imagen:
        producto.imagen.delete()
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
            messages.success(request, 'Pedido Modificado')
            return redirect('pedidos')
    return render(request, 'Otaku_ody/modificarpedido.html', {'form': form})

@admin_required
def eliminarpedido(request, id):
    tipoproducto = get_object_or_404(Pedido, id=id)
    tipoproducto.delete()
    messages.warning(request, 'Pedido Eliminado')
    return redirect('pedidos')

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
    total_pedidos = Pedido.calcular_total_todos_pedidos()
    return render(request, 'Otaku_ody/estadisticas.html', {'total_pedidos': total_pedidos})


# Vista de prueba
def test(request):
    productos = Producto.objects.all()
    return render(request, 'Otaku_ody/test.html', {'productos': productos})

@login_required
def carrito(request):
    return render(request, 'Otaku_ody/carrito.html')

def get_or_create_cart(request):
    if request.user.is_authenticated:
        carrito = Carrito.objects.filter(usuario=request.user).first()
        if not carrito:
            carrito = Carrito.objects.create(usuario=request.user)
    else:
        session_key = request.session.session_key or request.session.create()
        carrito = Carrito.objects.filter(session_key=session_key).first()
        if not carrito:
            carrito = Carrito.objects.create(session_key=session_key)
    return carrito

@login_required
def agregar_al_carrito(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    carrito = get_or_create_cart(request)
    
    if request.method == 'POST':
        cantidad = int(request.POST.get('cantidad', 1))
        if cantidad < 1:
            messages.error(request, "La cantidad debe ser al menos 1.")
            return redirect('t_productos')
        
        item, item_created = ItemCarrito.objects.get_or_create(carrito=carrito, producto=producto)
        if not item_created:
            item.cantidad += cantidad
        else:
            item.cantidad = cantidad
        item.save()
    
    return redirect('ver_carrito')

@login_required
def actualizar_carrito(request, item_id):
    item = get_object_or_404(ItemCarrito, id=item_id)
    if request.method == 'POST':
        cantidad = int(request.POST.get('cantidad', 1))
        if cantidad < 1:
            messages.error(request, "La cantidad debe ser al menos 1.")
        else:
            item.cantidad = cantidad
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
def limpiar_carrito(request):
    carrito = get_or_create_cart(request)
    carrito.items.all().delete()
    return redirect('index')

@login_required
def crear_pedido(request):
    
    if request.method == 'POST':
        # Obtener los datos del formulario
        metodo_pago = request.POST.get('metodo_pago')
        cardNumber = request.POST.get('cardNumber')
        expiration_date = request.POST.get('expirationDate')
        cvv = request.POST.get('cvv')
        cardholder_name = request.POST.get('cardholderName')
        address = request.POST.get('address')
        region = request.POST.get('region')
        comuna = request.POST.get('comuna')
        metodo_envio = request.POST.get('metodo_envio')
        phone = request.POST.get('phone')
        recipient_name = request.POST.get('recipientName')
        recipient_last_name = request.POST.get('recipientLastName')
        rut = request.POST.get('rut')

        # Validar y procesar los datos según sea necesario
        
        # Crear el pedido
        if pedido:
            pedido.metodo_pago = metodo_pago
            pedido.direccion_entrega = address
            pedido.region = region
            pedido.comuna = comuna
            pedido.metodo_envio = metodo_envio
            pedido.telefono = phone
            pedido.nombre_receptor = recipient_name
            pedido.apellido_receptor = recipient_last_name
            pedido.rut = rut
            pedido.save()
        else:
            pedido = Pedido.objects.create(
                usuario=request.user,
                metodo_pago=metodo_pago,
                direccion_entrega=address,
                region=region,
                comuna=comuna,
                metodo_envio=metodo_envio,
                telefono=phone,
                nombre_receptor=recipient_name,
                apellido_receptor=recipient_last_name,
                rut=rut
            )
    carrito = get_or_create_cart(request)
    
    if not carrito.items.exists():
        messages.error(request, "No puedes crear un pedido con un carrito vacío.")
        return redirect('ver_carrito')
    
    pedido = Pedido.objects.create(usuario=request.user)
    
    for item in carrito.items.all():
        if item.producto.stock < item.cantidad:
            pedido.delete()  # Eliminar el pedido si no hay suficiente stock
            messages.error(request, f'No hay suficiente stock para el producto {item.producto.nombre}')
            return redirect('ver_carrito')
        
        item.producto.stock -= item.cantidad
        item.producto.save()
        
        PedidoProducto.objects.create(pedido=pedido, producto=item.producto, cantidad=item.cantidad)
    
    pedido.calcular_total()
    
    carrito.items.all().delete()
    
    messages.success(request, "Pedido creado con éxito.")
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
