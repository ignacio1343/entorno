"""
URL configuration for Otaku_od project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from Aplicacion import views
from django.conf import settings
from django.conf.urls.static import static
from .views import preguntas, pedidos_user, t_productos, contacto, administracion, listaproducto, agregarproducto,modificarproducto,eliminarproducto,usuarios,\
        agregarusuario,modificarusuario,eliminarusuario,registro, carrito

urlpatterns = [
    path('', views.index, name='index'),
    path('preguntas/', preguntas, name='preguntas'),
    path('pedidos_user/', pedidos_user, name='pedidos_user'),
    path('t_productos/', t_productos, name='t_productos'),
    path('contacto/', contacto, name='contacto'),
    path('administracion/', administracion, name='administracion'),
    path('listaproducto/', listaproducto, name='listaproducto'),
    path('agregarproducto/', agregarproducto, name='agregarproducto'),
    path('modificarproducto/<id>/', modificarproducto, name='modificarproducto'),
    path('eliminarproducto/<id>/', eliminarproducto, name='eliminarproducto'),
    path('usuarios/', usuarios, name='usuarios'),
    path('agregarusuario/', agregarusuario, name='agregarusuario'),
    path('modificarusuario/<id>/', modificarusuario, name='modificarusuario'),
    path('eliminarusuario/<id>/', eliminarusuario, name='eliminarusuario'),
    path('registro/', registro, name='registro'),
    path('carrito/', carrito, name='carrito'),
]

if settings.DEBUG:
    urlpatterns+=static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)