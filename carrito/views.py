from django.shortcuts import render, redirect
from .models import Carrito
from api.models import Arma
from django.http import HttpResponseRedirect,HttpResponse
from django.urls import reverse
# Create your views here.

def view_compras(request):
    carrito = Carrito()

    precio_total = carrito.obtener_precio_total()
    armas_totales = carrito.obtener_armas()

    context = {'precio_total':precio_total,'armas_totales':armas_totales}

    return render(request,'compras_usuario.html',context)

def agregar_producto(request,arma_id):
    carrito = Carrito(request)
    arma = Arma.objects.get(id=arma_id)
    carrito.agregar(arma)
    return redirect(reverse('items'))

def eliminar_producto(request,arma_id):
    carrito = Carrito(request)
    arma= Arma.objects.get(id=arma_id)
    carrito.eliminar(arma)
    return redirect(reverse('tienda'))

def restar_producto(request,arma_id):
    carrito = Carrito(request)
    arma= Arma.objects.get(id=arma_id)
    carrito.restar_arma(arma)
    return redirect(reverse('tienda'))

def limpiar_carrito(request):
    carrito = Carrito(request)
    carrito.limpiar()
    return redirect(reverse('tienda'))


def tienda(request):
    armas = Arma.objects.all()

    return render(request,'tienda.html',{'armas':armas})

