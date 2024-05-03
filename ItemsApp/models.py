from django.db import models

# Create your models here.

class Arma(models.Model):
    itemid = models.CharField(max_length=13)
    defindex = models.IntegerField(blank=True, null=True)
    paintseed =  models.IntegerField(blank=True, null=True) #Campo importante para ver los valores de las skins case hardened por ejemplo
    rarity = models.IntegerField(blank=True, null=True)
    quality = models.IntegerField(blank=True, null=True) 
    killeatervalue = models.IntegerField(blank=True, null=True) # Contador de kills del statrak
    customname = models.CharField(max_length=100,blank=True, null=True) #Si tiene nametag cual es el nombre
    stickers = models.JSONField(blank=True, null=True) #Si tiene stickers 
    floatvalue = models.FloatField(blank=True, null=True) #Valor del float
    imageurl = models.URLField(max_length=1000) # Esto habra que modificarlo en su debido momento para mostrar las imagenes en las vistas.
    min = models.FloatField(blank=True, null=True) #Float mínimo posible del arma
    max = models.FloatField(blank=True, null=True) #Float máximo posible del arma
    item_name = models.CharField(max_length=100) #Nombre de la skin, por ejemplo Redline para el AK-47
    weapon_type = models.CharField(max_length=50) #Nombre del arma, por ejemplo AK-47
    origin_name = models.CharField(max_length=100) #Si proviene de una caja o un tradeup
    quality_name = models.CharField(max_length=100) #Si el arma es de tipo Souvenir,Statrak,Unique etc
    rarity_name = models.CharField(max_length=100) #Si el armas es de tipo clasified,Milspec
    wear_name = models.CharField(max_length=100) #Si el arma esta en factory new, minimalwear, etc
    full_item_name = models.CharField(max_length=100) #Nombre completo del arma, por ej: SSG 08 Blue Spruce (Minimal Wear)
    categoria = models.CharField(max_length=100, default = None, blank=True, null=True)
    s = models.IntegerField(blank=True, null=True) #Estos parametros son importantes para obtener el float del arma. No todos los campos son obligatorios.
    a = models.IntegerField(blank=True, null=True)
    d = models.IntegerField(blank=True, null=True)
    m = models.IntegerField(blank=True, null=True)
    precio = models.FloatField(blank=True, null=True) 

"""
Categorias para las armas:
{'Pistols': [CZ75-Auto,Desert Eagle,Dual Berettas,Five-SeveN,Glock-18,P2000,P250,R8 Revolver,Tec-9,USP-S]
 'Rifles': [AK-47,AUG,AWP,FAMAS,G3SG1,Galil AR, M4A1-S, M4A4, SCAR-20, SG553, SSG 08]
 'SMG': [MAC-10, MP5-SD, MP7, MP9, PP-Bizon, P90, UMP-45]
 'Heavy': [MAG-7, Nova, Sawed-Off, XM1014, M249, Negev]
 'Knives': [Bayonet, Bowie Knife, Butterfly Knife, Classic Knife, Falchion Knife, Flip Knife, Gut Knife, Huntsman Knife, Karambit, M9 Bayonet, Navaja Knife, Nomad Knife, Paracord Knife, Shadow Daggers,Skeleton Knife, Stiletto Knife, Survival Knife, Talon, Knife, Ursus Knife, Kukri Knife]}

"""