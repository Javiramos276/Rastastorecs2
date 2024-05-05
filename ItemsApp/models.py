from django.db import models
import json
import requests
import sys
from pprint import pprint 
import time
import psycopg2  # Importa la librería psycopg2 para conectarte a PostgreSQL
from api.models import Arma
import os

# Create your models here.
class ItemHandler():

    def __init__(self):
        self.processed_links = set() #Defino un conjunto donde voy a guardar las links que ya analice
        self.load_processed_links() #Los cargo porque los guarde en disco

    def load_processed_links(self):
        if os.path.exists("processed_links.txt"):
            with open("processed_links.txt", "r") as f:
                self.processed_links = set(f.read().splitlines())

    def save_processed_links(self, link):
        self.processed_links.add(link)  # Agregar el nuevo enlace al conjunto
        with open("processed_links.txt", "w") as f:
            f.write("\n".join(self.processed_links))

    def obtenertxt(self):
        json_data2 = (requests.get("https://steamcommunity.com/inventory/76561199092801246/730/2")).json()                           
        with open('jsonitemsrasta.txt','w', encoding="utf-8") as file:
            json.dump(json_data2, file)

    def filtraritem(self):
        with open(r'C:\Users\Ramos\Desktop\PYTHON_JAVI_NOTEMETASDIEGO\Rastastore_django\RastastoreProyecto\ItemsApp\jsonitemsrasta.txt','r', encoding='utf-8-sig') as f:
            content = f.read()
            data = json.loads(content) #Data es un objeto que contiene descriptions y assets
            return data

    def steam_links(self):
        data = self.filtraritem() #Data es un diccionario de objetos que contiene la informacion de todos los objetos
        
        links = []
        for item in data['assets']:
            classid = item['classid']
            owner_steamid = '76561199092801246'
            for description in data['descriptions']:
                if description['classid'] == classid:
                    if 'actions' in description and description['actions']:
                        assetid = item['assetid']
                        link = description['actions'][0]['link']
                        # Reemplazar assetid por classid en el enlace
                        modified_link = link.replace(r'%assetid%', assetid)
                        # Reemplazar owner_steamid en el enlace
                        modified_link = modified_link.replace(r'%owner_steamid%', owner_steamid)
                        links.append(modified_link)
        return links
    

    def links_processed(self,first_3_links):
        fields = [
            'origin',
            'quality' ,
            'rarity',
            'a',
            'd',
            'paintseed',
            'defindex',
            'paintindex',
            'floatid',
            'floatvalue',
            'full_item_name',
            'imageurl',
            'max',
            'min',
            'quality_name',
            'weapon_type',
            'wear_name',
            'low_rank',
            'high_rank',
            's',
            'm',
            'item_name',
            'rarity_name',
            'origin_name',
            'inspect_link',
        ]
        
        links = self.steam_links()
        for link in links:
            if link in self.processed_links:
                print(f"El enlace {link} ya ha sido procesado. Saltando...")
            else:
                json_data = requests.get(f"http://localhost/?url="+link)
                time.sleep(1)
                if json_data.status_code == 200:
                    content = json_data.json()
                    item_info = content.get('iteminfo')
                    my_data = {field: item_info.get(field, None) for field in fields}
                    my_data['inspect_link'] = link #Agrego manualmente el link de inspeccion porque no me lo da el request que estoy haciendo.
                    arma = Arma(**my_data) #El ** desempaqueta un diccionaro y le pasa a Arma las claves y el valor
                    arma.save()
                    print('item cargado exitosamente.')
                    self.save_processed_links(link)
                else:
                    print(f"La solicitud a {json_data} no fue exitosa. Código de estado:", json_data.status_code)
                    #Aca tengo que hacer un retry si la informacion no entro bien. Despues veo como hacerlo. De momento funciona. Usar bucle while!!!!
        
class Carrito():

    def __init__(self):
        self.items = []
    
    def sumar_al_carrito(self,arma):
        #Agrega items al carrito de compras
        self.items.append(arma)

    def sacar_del_carrito(self,arma):
        #Quita items del carrito de compras
        if self.items: #Eso significa que si la lista no esta vacía
            if arma in self.items:  # Si el arma está en la lista
                self.items.remove(arma)

    def obtener_armas(self):
        #Devuelve una lista con todas armas
        armas = []
        for arma in self.items:
            armas.append(arma)
        return armas

    def obtener_precio_total(self):
        #Obtiene el precio total del carrito
        total = 0
        for arma in self.items:
            total += arma.precio  # para cada arma, sumamos el total de su precio y lo retornamos
        return total



