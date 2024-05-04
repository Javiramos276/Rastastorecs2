from django.db import models
import json
import requests
import sys
from pprint import pprint 
import time
import psycopg2  # Importa la librería psycopg2 para conectarte a PostgreSQL
from api.models import Arma

# Create your models here.
class ItemHandler():

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
        ]
        
        links = self.steam_links()
        for link in first_3_links:
            json_data = requests.get(f"http://localhost/?url="+link)
            time.sleep(1)
            if json_data.status_code == 200:
                content = json_data.json()
                item_info = content.get('iteminfo')
                my_data = {field: item_info.get(field, None) for field in fields}
                arma = Arma(**my_data) #El ** desempaqueta un diccionaro y le pasa a Arma las claves y el valor
                arma.save()
                print('item cargado exitosamente.')
            else:
                print(f"La solicitud a {json_data} no fue exitosa. Código de estado:", json_data.status_code)
                #Aca tengo que hacer un retry si la informacion no entro bien. Despues veo como hacerlo. De momento funciona. Usar bucle while!!!!
    