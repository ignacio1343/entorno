from django.shortcuts import render, redirect, get_object_or_404
from .models import Producto
from .forms import ProductoForm
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
        else:
            data["mensaje"] = formulario
    
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


def test(request):
    productos = Producto.objects.all()
    data = {
        'productos': productos
    }
    return render(request, 'Otaku_ody/test.html', data)