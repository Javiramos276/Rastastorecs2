from django.db import models
from Usuarios.models import CustomUser

# Create your models here.

class Carrito(models.Model):

    usuario = models.ForeignKey(CustomUser, related_name="subcategories",on_delete=models.CASCADE, default=None)

    def __init__(self,request):
        self.request = request
        self.session = request.session
        if 'carrito' not in self.session:
            self.session['carrito'] = {}
        self.carrito = self.session['carrito']


    def agregar(self,arma):
        id = str(arma.id)
        if id not in self.carrito.keys():
            self.carrito[id]={
                "id_arma":arma.id,
                "nombre_completo_arma":arma.full_item_name,
                "imagen_arma":(arma.imageurl), #.replace('%3A', ':').replace('%2F', '/').lstrip('/'), 
                "acumulado": arma.precio,
                "cantidad":1,
                "float": arma.floatvalue,
            }
        else:
            self.carrito[id]["cantidad"] +=1
            self.carrito[id]["acumulado"] += arma.precio
        self.guardar_carrito()

    def guardar_carrito(self):
        self.session["carrito"] = self.carrito
        self.session.modified = True

    def eliminar(self,arma):
        id = str(arma.id)
        if id in self.carrito:
            del self.carrito[id]
            self.guardar_carrito()

    def restar_arma(self,arma):
        id= str(arma.id)
        if id in self.carrito.keys():
            self.carrito[id]["cantidad"] -= 1
            self.carrito[id]["acumulado"] -= arma.precio
            if self.carrito[id]["cantidad"] <= 0: self.eliminar(arma)
            self.guardar_carrito()

    def limpiar(self):
        self.session["carrito"] = {}
        self.session.modified = True

