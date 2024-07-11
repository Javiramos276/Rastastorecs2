from django.db import models
import json
import requests
import sys
from pprint import pprint 
import time
import psycopg2  # Importa la librería psycopg2 para conectarte a PostgreSQL
from api.models import Arma
import os
import re
from bs4 import BeautifulSoup

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
        


    def steam_links_and_desc(self,owner_name,owner_steamid):
    
        data = self.filtraritem(owner_name) #Data es un diccionario de objetos que contiene la informacion de todos los objetos

        informacion_items = []
        for item in data['assets']:
            classid = item['classid'] #Buscamos en el diccionario de assets el classid
            instanceid = item['instanceid']
            for description in data['descriptions']:
                if description['classid'] == classid and description['instanceid'] == instanceid: #Relacionamos los objetos con el classid
                    # descriptions.append(description)
                    informacion_item = {}
                    if 'actions' in description and description['actions']: #Vemos si tienen opcion para inspeccionar en el juego
                        assetid = item['assetid']
                        link = description['actions'][0]['link']
                        # Reemplazar assetid por classid en el enlace
                        modified_link = link.replace(r'%assetid%', assetid)
                        # Reemplazar owner_steamid en el enlace
                        modified_link = modified_link.replace(r'%owner_steamid%', str(owner_steamid))
                        informacion_item['modified_link'] = modified_link
                        # links.append(modified_link)

                    #Obtener el nombre de la etiqueta localizada usando la función obtener_tag_name
                    tags = description.get('tags', [])
                    localized_tag_name = self.obtener_tag_name(tags)
                    if localized_tag_name:
                        informacion_item['localized_tag_name'] = localized_tag_name
                    
                    #Aquí se agrega la información de los stickers
                    stickers_info = self.obtener_stickers_info(description['descriptions'])
                    if stickers_info:
                        informacion_item['stickers_info'] = stickers_info

                    # Añadir el diccionario de información del objeto a la lista
                    informacion_items.append(informacion_item)

        return informacion_items
                
    def obtener_tag_name(self, tags):
        for tag in tags:
            if tag['category'] == 'Type':
                return tag['localized_tag_name']
        return None  # Devuelve None si no encuentra ningún tag


    def obtener_stickers_info(self,descriptions):   
        stickers_info = []

        for item in descriptions:
            if 'sticker_info' in item['value']:
                sticker_info = item['value']

                soup = BeautifulSoup(sticker_info, 'html.parser')
                images = [img['src'] for img in soup.find_all('img')]
                text = soup.get_text(strip=True)
                sticker_names_matches = re.findall(r'Sticker: (.+)', text)

                if sticker_names_matches:
                    sticker_names = sticker_names_matches[0].split(',')
                else:
                    sticker_names = []

                for img, name in zip(images, sticker_names):
                    stickers_info.append({'sticker_img': img, 'sticker_name': name.strip()})

                # Si encontramos stickers, devolvemos la info del primero encontrado
                return stickers_info

        return None  # Devuelve None si no se encuentra información de stickers

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
            'localized_tag_name',
            'stickers_custom',
        ]
        
        informacion_items = self.steam_links_and_desc(owner_name,owner_steamid) #Recuerdo que items info es una lista con un dic adentro [{}]

        for item in informacion_items:
            print(item)
            if 'modified_link' in item:
                link = item['modified_link']
                if not Arma.objects.filter(inspect_link=link).exists():
                    json_data = requests.get(f"http://localhost/?url=" + link)
                    time.sleep(1)

                    if json_data.status_code == 200:
                        content = json_data.json()
                        item_info = content.get('iteminfo')
                        my_data = {field: item_info.get(field, None) for field in fields}
                        my_data['inspect_link'] = link
                        my_data['owner_steamid'] = owner_steamid
                        my_data['precio'] = 0
                        if 'localized_tag_name' in item:
                            my_data['localized_tag_name'] = item['localized_tag_name']
                        if 'stickers_info' in item:
                            my_data['stickers_custom'] = item['stickers_info']

                        arma = Arma(**my_data)
                        arma.save()
                        print(f'Item cargado exitosamente: {arma}')
                    else:
                        print(f"La solicitud a {item['inspect_link']} no fue exitosa. Código de estado:", json_data.status_code)
                        #Aca tengo que hacer un retry si la informacion no entro bien. Despues veo como hacerlo. De momento funciona. Usar bucle while!!!!
                else:
                    print(f"Esta arma ya existe en la base de datos")
        
    



