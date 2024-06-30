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
from django.urls import path
from Aplicacion import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('preguntas/', views.preguntas, name='preguntas'),
    path('pedidos_user/', views.pedidos_user, name='pedidos_user'),
    path('t_productos/', views.t_productos, name='t_productos'),
    path('contacto/', views.contacto, name='contacto'),
    path('administracion/', views.administracion, name='administracion'),
    path('listaproducto/', views.listaproducto, name='listaproducto'),
    path('agregarproducto/', views.agregarproducto, name='agregarproducto'),
    path('modificarproducto/<id>/', views.modificarproducto, name='modificarproducto'),
    path('eliminarproducto/<id>/', views.eliminarproducto, name='eliminarproducto'),
    path('usuarios/', views.usuarios, name='usuarios'),
    path('agregarusuario/', views.agregarusuario, name='agregarusuario'),
    path('modificarusuario/<id>/', views.modificarusuario, name='modificarusuario'),
    path('eliminarusuario/<id>/', views.eliminarusuario, name='eliminarusuario'),
    path('login/', views.login, name='login'),
        path('carrito/', views.carrito, name='carrito'),
]

if settings.DEBUG:
    urlpatterns+=static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)