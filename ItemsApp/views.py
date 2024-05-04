from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView, ListView
from .models import ItemHandler


def view_home(request):
    # Instancio el ItemHandler
    item_handler = ItemHandler()
    
    # Obtenemos los datos de la url y los links
    data = item_handler.filtraritem()
    links = item_handler.steam_links()

    # Proceso los primeros 3 links para probar
    first_3_links = links[:3]
    item_handler.links_processed(first_3_links)

    # Renderizar la vista
    return render(request, 'home.html', {'data': data, 'first_3_links': first_3_links})


    
