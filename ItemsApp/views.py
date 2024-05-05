from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView, ListView
from .models import ItemHandler, Arma, Carrito


def view_home(request):
    
    
    #Llamo a mi objeto de armas y obtengo todas las armas de mi objeto Arma
    armas= Arma.objects.all()

    # Renderizar la vista
    return render(request, 'home.html', {'armas':armas})

def view_cargar_objetos(request):
    # Instancio el ItemHandler
    item_handler = ItemHandler()
    
    # Obtenemos los links que vamos a procesar
    links = item_handler.steam_links()

    # Proceso los primeros 10 links para probar
    first_3_links = links[:10]
    item_handler.links_processed(first_3_links)

def view_compras(request):
    carrito = Carrito()

    precio_total = carrito.obtener_precio_total()
    armas_totales = carrito.obtener_armas()

    context = {'precio_total':precio_total,'armas_totales':armas_totales}

    return render(request,'compras_usuario.html',context)