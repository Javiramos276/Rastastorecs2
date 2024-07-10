from django.db import models
from django.utils import timezone
from Usuarios.models import CustomUser
import uuid

# Create your models here.

class Carrito(models.Model):

    usuario = models.OneToOneField(CustomUser, related_name="carrito",on_delete=models.CASCADE, default=None)
    
    def agregar(self,arma):
        if not self.armas.filter(id=arma.id).exists(): #Si el arma no existe entonces la guardo
            arma.carrito = self
            arma.save()
            self.guardar_carrito()
            
    def eliminar(self,arma):
        if self.armas.filter(id=arma.id).exists():
            arma.carrito = None
            arma.save()
            self.guardar_carrito()

    def guardar_carrito(self):
        self.save()

    def total_carrito(self):
        total = sum(arma.precio for arma in self.armas.all())
        return total
        
    def limpiar(self,armas):
        for arma in armas:
            self.armas.remove(arma)
        
        self.guardar_carrito()

    def obtener_carrito(self):
        total = self.total_carrito()
        armas = self.armas.all()
        return {
            'armas': armas,
            'total': total
        }

class Compra(models.Model):
    ESTADOS_COMPRA = (
        ('Pendiente', 'Pendiente'),
        ('Cancelada', 'Cancelada'),
        ('Completada', 'Completada'),
    )
    
    transaccion_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    fecha_de_compra = models.DateTimeField(verbose_name='Fecha de compra',default=timezone.now)
    usuario = models.ForeignKey(CustomUser,related_name='compras',on_delete=models.SET_NULL, null=True) # Si se llegase a eliminar el usuario, este quedará en Null pero no se eliminará su compra.
    estado = models.CharField(max_length=10, choices=ESTADOS_COMPRA, default='Pendiente')


    def __str__(self):
        return f'Compra realizada por {self.usuario} a las {self.fecha_de_compra}. Id de transacción: {self.transaccion_id}'

    def verificar_objetos(self,armas):
        """
        Este método se encarga de verificar si los objetos cargados a Compra
        se encuentran disponibles al momento de realizar la compra.
        """
        if len(armas) == 0:
            return { 'status': 'Fallido','descripcion': "No se ha cargado ningun arma al carrito."}
        
        for arma in armas:
            if not arma.habilitada:
                self.estado = 'Cancelada'
                return {'status': 'Fallido', 'descripcion': f'El arma {arma.full_item_name} no se encuentra disponible o ya fue comprada por otro usuario.'}
        
        self.estado = 'Pendiente'
        self.save()
        
        for arma in armas:
            arma.habilitada = False
            arma.compra = self
            arma.save()
        
        return {'status':'Exitoso', 'descripcion':'Compra realizada con éxito y en estado pendiente.'}
        
    def confirmar_estado_compra(self,estado):
        """
        Una vez realizada la compra por el usuario, un administrador definirá si el 
        estado de la compra es Completado o Cancelado.
        """
        self.estado = estado
        if estado == 'Cancelada':
            for arma in self.armas_compradas.all():
                arma.habilitada = True
                arma.compra = self #Aunque se cancele la compra por las dudas guardo las armas
                arma.save()
            print('Compra cancelada')
        elif estado == 'Completada':
            print('Compra completada.')

        self.save()
     
    def total_compra(self):
        total = sum(arma.precio for arma in self.armas_compradas.all())
        return total
