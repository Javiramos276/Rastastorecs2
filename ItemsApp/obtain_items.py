import json
import requests
import sys
from pprint import pprint 
import time
import psycopg2  # Importa la librería psycopg2 para conectarte a PostgreSQL

# Conecta a la base de datos PostgreSQL (asegúrate de reemplazar estos valores con los tuyos)
conn = psycopg2.connect(
    dbname="rastastoredb",
    user="postgres",
    password="admin",
    host="localhost",
    port="5432"
)
cur = conn.cursor()

def obtenertxt():
    json_data2 = (requests.get("https://steamcommunity.com/inventory/76561199092801246/730/2")).json()                           
    with open('jsonitemsrasta.txt','w', encoding="utf-8") as file:
        json.dump(json_data2, file)

diccionario = {}
def filtraritem():
    with open(r'C:\Users\Ramos\Desktop\PYTHON_JAVI_NOTEMETASDIEGO\Rastastore_django\RastastoreProyecto\ItemsApp\jsonitemsrasta.txt','r', encoding='utf-8-sig') as f:
        content = f.read()
        data = json.loads(content) #Data es un objeto que contiene descriptions y assets
        return data

# def obtener_info_armas():
#     info_completa = requests.get("http://localhost/?url=steam://rungame/730/76561202255233023/+csgo_econ_action_preview%20S76561198169110373A35549439647D5354371389195572357")
#     print(info_completa)
#     print(info_completa.text)

def descriptions():
    data = filtraritem() #Data es un diccionario de objetos que contiene la informacion de todos los objetos
    
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

    for link in links:
        json_data = requests.get(f"http://localhost/?url="+link)
        time.sleep(1)
        if json_data.status_code == 200:
            content = json_data.json()
            item_info = content.get('iteminfo')
            my_data = [item_info.get(field, None) for field in fields]
            # Crear la cadena de marcadores de posición para la consulta SQL
            placeholders = ', '.join(['%s'] * len(fields))
            # Crear la consulta SQL con los campos y marcadores de posición
            sql_query = f"INSERT INTO items ({', '.join(fields)}) VALUES ({placeholders})"
            cur.execute(sql_query, my_data)
            conn.commit()
            print('item cargado exitosamente.')

    
        else:
            print("La solicitud no fue exitosa. Código de estado:", json_data.status_code)
    
    
    


# obtenertxt()
#filtraritem()
descriptions()
cur.close()
conn.close()

#obtener_info_armas()
