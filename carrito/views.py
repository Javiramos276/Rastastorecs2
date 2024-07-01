from django.shortcuts import render, redirect
from .models import Carrito
from api.models import Arma
from django.http import HttpResponseRedirect,HttpResponse
from django.urls import reverse
# Create your views here.

def view_compras(request):
    carrito = Carrito()

    precio_total = carrito.total_carrito()
    armas_totales = carrito.obtener_carrito()

    context = {'precio_total':precio_total,'armas_totales':armas_totales}

    return render(request,'compras_usuario.html',context)

def agregar_producto(request,arma_id):
    if request.method == "POST":
        carrito,created = Carrito.objects.get_or_create(usuario=request.user) #El metodo get_or_create retorna una tupla, el carrito y "creado" que es un booleano
        arma = Arma.objects.get(id=arma_id)
        carrito.agregar(arma)
    return redirect(reverse('items'))

def eliminar_producto(request,arma_id):
    carrito,created = Carrito.objects.get_or_create(usuario=request.user)
    arma = Arma.objects.get(id=arma_id)
    carrito.eliminar(arma)
    return redirect(reverse('tienda'))

def restar_producto(request,arma_id):
    carrito = Carrito(request)
    arma= Arma.objects.get(id=arma_id)
    carrito.restar_arma(arma)
    return redirect(reverse('tienda'))

def limpiar_carrito(request):
    carrito,created = Carrito.objects.get_or_create(usuario=request.user)
    carrito.limpiar()
    return redirect(reverse('tienda'))

def tienda(request):
    carrito,created = Carrito.objects.get_or_create(usuario=request.user)
    contenido_carrito = carrito.obtener_carrito()
    total_carrito = carrito.total_carrito()

    return render(request,'tienda.html',{'armas': contenido_carrito, 'total_carrito': total_carrito})

