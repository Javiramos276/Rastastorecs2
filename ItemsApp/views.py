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
    
    owner_steamid = {
            "Rasta":76561199092801246,
            "Fell":76561198085469210 ,
        }
    
    # Obtenemos el txt del inventario de cada uno
    # item_handler.obtenertxt()

    # Filtramos la informacion
    for owner_name,owner_id in owner_steamid.items(): #Aca no se si es necesario pasar owner_name, pero como se trata de un dict lo dejo
        print(f'el owner_name es {owner_name}')
        print(f'el owner_id es {owner_id}')
        item_handler.links_processed(owner_name, owner_id)

    return HttpResponse("Los enlaces se estan procesando.")

    
    

    

def view_compras(request):
    carrito = Carrito()

    precio_total = carrito.obtener_precio_total()
    armas_totales = carrito.obtener_armas()

    context = {'precio_total':precio_total,'armas_totales':armas_totales}

    return render(request,'compras_usuario.html',context)