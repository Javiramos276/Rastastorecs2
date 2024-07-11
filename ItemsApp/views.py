from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from django.views.generic import TemplateView, ListView
from .models import ItemHandler, Arma
from django.db.models import Q #Permite hacer consultas complejas 

def get_estado(float_value):
    #El objetivo de esta funcion es retornar el estado del arma para luego en el css poder llenar la barrita en su color correspondiente.
    if float_value <= 0.07:
        return 'estado-factory-new'
    elif float_value <= 0.15:
        return 'estado-minimal-wear'
    elif float_value <= 0.37:
        return 'estado-field-tested'
    elif float_value <= 0.44:
        return 'estado-well-worn'
    else:
        return 'estado-battle-scarred'

def view_pistolas_filter(request):
    weapon_type = ['Desert Eagle','P250','USP-S','Glock-18','Tec-9']
    armas= Arma.objects.all().filter(weapon_type__in=weapon_type)

    context = {'armas':armas}
    return render(request,'items.html',context)

def view_rifles_filter(request):
    weapon_type = ['FAMAS','AK-47','AWP','M4A1-S','G3SG1','M4A4','SCAR-20','SSG 08']
    armas= Arma.objects.all().filter(weapon_type__in=weapon_type)

    context = {'armas':armas}
    return render(request,'items.html',context)

def view_factorynew_filter(request):
    armas= Arma.objects.all().filter(floatvalue__lt = 0.07) #floatvalue__lt significa less_than en mi campo floatvalue


    # Filtro por weapon_type excluyendo los valores de la lista
    weapon_type_exclude = ['Service Medal', 'Graffiti','Diamond Operation Broken Fang Coin','Diamond Operation Shattered Web Coin',
                           '2019 Service Medal','Sticker','Service Medal','Michael Syfers  | FBI Sniper','Global Offensive Badge',
                           '2023 Service Medal','2024 Service Medal','2022 Service Medal','2021 Service Medal','2020 Service Medal',
                           '2018 Service Medal','2017 Service Medal','2016 Service Medal','5 Year Veteran Coin','Loyalty Badge',
                           'Silver Operation Hydra Coin','10 Year Birthday Coin','Diamond Operation Riptide Coin','Operation Bloodhound Challenge Coin',
                           "'The Doctor' Romanov | Sabre"]
    
    armas = armas.exclude(weapon_type__in=weapon_type_exclude)
    
    for arma in armas:
        arma.floatvalue = "{:.6f}".format(arma.floatvalue) #Recortamos el valor del float a 6 digitos

    context = {'armas':armas}
    return render(request,'items.html',context)



def view_home(request):
    
    weapon_type = ['Service Medal', 'Graffiti','Diamond Operation Broken Fang Coin','Diamond Operation Shattered Web Coin',
                   '2019 Service Medal','Sticker','Service Medal','Michael Syfers  | FBI Sniper','Global Offensive Badge',
                   '2023 Service Medal','2024 Service Medal','2022 Service Medal','2021 Service Medal','2020 Service Medal',
                   '2018 Service Medal','2017 Service Medal','2016 Service Medal','5 Year Veteran Coin','Loyalty Badge',
                   'Silver Operation Hydra Coin','10 Year Birthday Coin','Diamond Operation Riptide Coin','Operation Bloodhound Challenge Coin',
                   "'The Doctor' Romanov | Sabre",]
    #Llamo a mi objeto de armas y obtengo todas las armas de mi objeto Arma
    armas= Arma.objects.all().filter(~Q(weapon_type__in=weapon_type))

    for arma in armas:
        arma.floatvalue = "{:.6f}".format(arma.floatvalue) #Recortamos el valor del float a 6 digitos

    
    # Renderizar la vista
    return render(request, 'items.html', {'armas':armas})

def nav_bar(request):
    return render(request,'nav.html')

def view_cargar_objetos(request):
    # Instancio el ItemHandler
    item_handler = ItemHandler()
    
    owner_steamid = {
            "Rasta":76561199092801246,
            # "Fell":76561198085469210 ,
        }
    
    # Obtenemos el txt del inventario de cada uno
    # item_handler.obtenertxt()

    # Filtramos la informacion
    for owner_name,owner_id in owner_steamid.items(): #Aca no se si es necesario pasar owner_name, pero como se trata de un dict lo dejo
        print(f'el owner_name es {owner_name}')
        print(f'el owner_id es {owner_id}')
        item_handler.links_processed(owner_name, owner_id)

    return HttpResponse("Los enlaces se estan procesando.")

def view_agregar_precio(request,arma_id):
    if request.method == 'POST':
        nuevo_precio = request.POST.get('nuevo_precio')
        if nuevo_precio:  # Verificar si se proporcionó un precio
            nuevo_precio = float(nuevo_precio)  # Convertir a tipo numérico #obtenemos el precio del formulario
            arma = Arma.objects.get(id=arma_id)
            arma.precio = nuevo_precio
            arma.save()
        else:
            print("El precio introducido no es válido")

    return redirect('items')
    
def view_eliminar_item(request,arma_id):
    if request.method == 'POST':
        arma = Arma.objects.get(id=arma_id)
        arma.delete()
        arma.save()

    return redirect('items')

def view_get_precios(request):
    #Mandamos la respuesta en formato Json

    armas = Arma.objects.all()
    data = serializers.serialize('json', armas)

    if (len(armas)>0):
        data = {'message':"Success", 'armas':data}
    else:
        data = {'message':"No encontrado"}
    
    return JsonResponse(data)
    
