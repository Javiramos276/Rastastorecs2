from django.db import models
from Usuarios.models import CustomUser

# Create your models here.

class Carrito(models.Model):

    usuario = models.OneToOneField(CustomUser, related_name="carrito",on_delete=models.CASCADE, default=None)

    def agregar(self,arma):
        id_arma = str(arma.id)
        if id_arma not in self.contenido_carrito:
            self.contenido_carrito[id_arma] = {
                        "id_arma":arma.id,
                        "nombre_completo_arma":arma.full_item_name,
                        "imagen_arma":(arma.imageurl), #.replace('%3A', ':').replace('%2F', '/').lstrip('/'), 
                        "precio": arma.precio,
                        "cantidad":1,
                        "float": arma.floatvalue,}
        else:
            self.contenido_carrito["cantidad"] += 1
        
        self.guardar_carrito()

    def eliminar(self,arma):
        id_arma = str(arma.id)
        if id_arma in self.contenido_carrito:
            del self.contenido_carrito[id_arma]
            self.guardar_carrito()

    def restar_arma(self,arma):
        id_arma = str(arma.id)
        if id_arma in self.contenido_carrito:
            if self.carrito[id_arma]["cantidad"] > 0:
                self.carrito[id_arma]["cantidad"] -= 1
                self.carrito[id_arma]["precio"] -= arma.precio
            else: 
                self.eliminar(arma)
        
        self.guardar_carrito()

    def guardar_carrito(self):
        self.save()

    def total_carrito(self):
        total = 0
        for id in self.contenido_carrito:
            total += self.contenido_carrito[id]["precio"] * self.contenido_carrito[id]["cantidad"]
        
        return total
        
    def limpiar(self):
        self.contenido_carrito = {}
        self.guardar_carrito()

    def obtener_carrito(self):
        return self.contenido_carrito

