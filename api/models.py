from django.db import models
from carrito.models import Carrito

# Create your models here.

class Arma(models.Model):
    origin = models.IntegerField(blank=True, null=True)
    quality = models.IntegerField(blank=True, null=True) 
    rarity = models.IntegerField(blank=True, null=True)
    a = models.CharField(max_length=255, blank=True, null=True)
    d = models.CharField(max_length=255, blank=True, null=True)
    paintseed = models.IntegerField(blank=True, null=True)
    defindex = models.IntegerField(blank=True, null=True)
    paintindex = models.IntegerField(blank=True, null=True)
    floatid = models.CharField(max_length=255, blank=True, null=True)
    floatvalue = models.FloatField(blank=True, null=True)
    full_item_name = models.TextField(blank=True, null=True)
    imageurl = models.URLField(blank=True, null=True,max_length=2000) 
    max = models.FloatField(blank=True, null=True)
    min = models.FloatField(blank=True, null=True)
    quality_name = models.CharField(max_length=255, blank=True, null=True)
    weapon_type = models.CharField(max_length=255, blank=True, null=True)
    wear_name = models.CharField(max_length=255, blank=True, null=True)
    low_rank = models.IntegerField(blank=True, null=True)
    high_rank = models.IntegerField(blank=True, null=True)
    s = models.CharField(max_length=255, blank=True, null=True)
    m = models.CharField(max_length=255, blank=True, null=True)
    item_name = models.CharField(max_length=255, blank=True, null=True)
    rarity_name = models.CharField(max_length=255, blank=True, null=True)
    origin_name = models.CharField(max_length=255, blank=True, null=True)
    precio = models.IntegerField(blank=True, null=True)  
    inspect_link = models.CharField(null=True,blank=True,max_length=2000) #Aca si utilizo un URLFIELD tengo problemas en el admin. Charfield me sirve y no genera errores
    owner_steamid = models.BigIntegerField(blank=False, default=76561199092801246)  #Cada arma siempre tiene que tener un propietario
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE, null=True, blank=True)