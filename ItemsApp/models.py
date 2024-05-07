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
class ItemHandler(models.Model):

    def obtenertxt(self):
        #Permite obtener un txt con los datos en crudo del endpoint con la informacion de los objetos
        owner_steamid = {
            "Rasta":76561199092801246,
            "Fell":76561198085469210,
        }
        for name, owner in owner_steamid.items():
            print(f'Realizando la petición para {name}...')
            #https://steamcommunity.com/inventory/{owner}/730/2?l=english&count=5000
            response = requests.get(f"https://steamcommunity.com/inventory/{owner}/730/2?l=english&count=5000")
            if response.status_code == 200:
                print(f'Petición realizada con éxito')                           
                json_data = response.json()
                with open(f'jsonitems_{name}.txt', 'w', encoding="utf-8") as file:
                    json.dump(json_data, file)
            else:
                print(f"Hubo un problema al realizar la petición, status_code ={response.status_code}")

    def filtraritem(self, owner_name):
        #Retorna los valores en un json 
        with open(f'jsonitems_{owner_name}.txt', 'r', encoding='utf-8') as f:
            content = f.read()
            data = json.loads(content)
            # Procesar los archivos por separado
            # datos_rasta = ItemHandler.filtraritem("Rasta")
            # datos_fell = ItemHandler.filtraritem("Fell")
            return data
        


    def steam_links(self,owner_name,owner_steamid):
    
        data = self.filtraritem(owner_name) #Data es un diccionario de objetos que contiene la informacion de todos los objetos
        
        links = []
        for item in data['assets']:
            classid = item['classid'] #Buscamos en el diccionario de assets el classid
            for description in data['descriptions']:
                if description['classid'] == classid: #Relacionamos los objetos con el classid
                    if 'actions' in description and description['actions']: #Vemos si tienen opcion para inspeccionar en el juego
                        assetid = item['assetid']
                        link = description['actions'][0]['link']
                        # Reemplazar assetid por classid en el enlace
                        modified_link = link.replace(r'%assetid%', assetid)
                        # Reemplazar owner_steamid en el enlace
                        modified_link = modified_link.replace(r'%owner_steamid%', str(owner_steamid))
                        links.append(modified_link)
        return links
    

    def links_processed(self,owner_name,owner_steamid):
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
            'owner_steamid',
            'precio',
        ]
        
        links = self.steam_links(owner_name,owner_steamid) 
        links = links[:50] #Solo retorno los primeros 10 para probar
        armas_existente  = Arma.objects.all() #Me traigo todas las armas de la base de datos
        for link in links:
            arma_existente = armas_existente.filter(inspect_link=link).exists()  #Verifico con un filtro si ya existe una arma con dicho link
            if arma_existente:
                print(f"El enlace {link} ya ha sido procesado. Saltando...")
            else:
                json_data = requests.get(f"http://localhost/?url="+link)
                time.sleep(1)
                if json_data.status_code == 200:
                    content = json_data.json()
                    item_info = content.get('iteminfo')
                    my_data = {field: item_info.get(field, None) for field in fields}
                    my_data['inspect_link'] = link #Agrego manualmente el link de inspeccion porque no me lo da el request que estoy haciendo.
                    my_data['owner_steamid'] = owner_steamid
                    my_data['precio'] = 0
                    arma = Arma(**my_data)  # Crear una nueva instancia de Arma con los datos
                    arma.save()
                    print('item cargado exitosamente.')
                else:
                    print(f"La solicitud a {link} no fue exitosa. Código de estado:", json_data.status_code)
                    
                    #Aca tengo que hacer un retry si la informacion no entro bien. Despues veo como hacerlo. De momento funciona. Usar bucle while!!!!
        




