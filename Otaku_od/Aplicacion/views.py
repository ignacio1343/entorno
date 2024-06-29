from django.shortcuts import render

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