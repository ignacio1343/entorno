from django.shortcuts import render
from .models import Producto
# Create your views here.

def index(request):
    
    return render(request, 'Otaku_ody/index.html')

def preguntas(request):
    return render(request, 'Otaku_ody/preguntas.html')

def v_itachi(request):
    return render(request, 'Otaku_ody/v_itachi.html')

def v_zenitsu(request):
    return render(request, 'Otaku_ody/v_zenitsu.html')

def pedidos_user(request):
    return render(request, 'Otaku_ody/pedidos_user.html')

def t_productos(request):
    return render(request, 'Otaku_ody/t_productos.html')

def contacto(request):
    return render(request, 'Otaku_ody/contacto.html')

def v_asuka(request):
    return render(request, 'Otaku_ody/v_asuka.html')

def v_goku(request):
    return render(request, 'Otaku_ody/v_goku.html')

def test(request):
    return render(request, 'Otaku_ody/test.html')

def test(request):
    productos = Producto.objects.all()
    data = {
        'productos': productos
    }
    return render(request, 'Otaku_ody/test.html')