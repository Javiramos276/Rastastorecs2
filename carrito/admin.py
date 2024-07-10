from django.contrib import admin
from django.utils.html import format_html
from .models import Carrito, Compra

class CompraAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'fecha_de_compra', 'transaccion_id', 'estado', 'listar_armas','total_de_compra')
    ordering = ('estado','fecha_de_compra')
    search_fields = ('transaccion_id',)
    list_editable = ('estado',)

    def listar_armas(self, obj):
        armas = obj.armas_compradas.all()  # Obtiene todas las armas asociadas a esta compra
        armas_list =  [arma.full_item_name for arma in armas]
        return format_html("<br>".join(armas_list))

    def total_de_compra(self, obj):
        return obj.total_compra()
    
    def save_model(self, request, obj, form, change): #Sacado de la docu de django https://docs.djangoproject.com/en/4.1/ref/contrib/admin/#django.contrib.admin.ModelAdmin.save_model
        print("se ejecuta el save de compra")
        if obj.estado in ['Completada', 'Cancelada']: #Si el estado el arma es Completada o Cancelada entonces se procede a finalizar el estado de la compra.
            obj.confirmar_estado_compra(obj.estado)
            print("confirmando estado de compra.")
        obj.save()


    listar_armas.short_description = 'Armas compradas'  # Nombre personalizado para la columna en el admin
    total_de_compra.short_description = 'Total de compra'

# Register your models here.
admin.site.register(Carrito)
admin.site.register(Compra,CompraAdmin)
