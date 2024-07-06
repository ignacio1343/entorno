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
from .views import preguntas, pedidos_user, t_productos, contacto,pedidos,\
        administracion, listaproducto, agregarproducto,modificarproducto,eliminarproducto,usuarios,\
        agregarusuario,modificarusuario,eliminarusuario,registro, carrito, estadisticas, pedidos
from .views import *
from rest_framework import routers

router = routers.DefaultRouter()
router.register('producto', ProductoViewset)

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
    path('estadisticas/', estadisticas, name='estadisticas'),
    path('pedidos/', pedidos, name='pedidos'),
    path('modificarpedido/<id>/', modificarpedido, name='modificarpedido'),
    path('eliminarpedido/<id>/', eliminarpedido, name='eliminarpedido'),
    path('agregartipoproducto/', agregartipoproducto, name='agregartipoproducto'),
    path('modificartipoproducto/<id>/', modificartipoproducto, name='modificartipoproducto'),
    path('eliminartipoproducto/<id>/', eliminartipoproducto, name='eliminartipoproducto'),
    path('tipoproducto/', tipoproducto, name='tipoproducto'),
    path('crearadmin/', crearadmin, name='crearadmin'),
    path('carrito/', carrito, name='carrito'),
    path('agregar-al-carrito/<int:producto_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('ver-carrito/', views.ver_carrito, name='ver_carrito'),
    path('eliminar-del-carrito/<int:item_id>/', views.eliminar_del_carrito, name='eliminar_del_carrito'),
    path('limpiar_carrito', limpiar_carrito, name='limpiar_carrito'),
    path('carrito/crear_pedido/', views.crear_pedido, name='crear_pedido'),
    path('pedido/<int:pedido_id>/', views.ver_pedido, name='ver_pedido'),
    path('api/', include(router.urls)),
]

if settings.DEBUG:
    urlpatterns+=static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)