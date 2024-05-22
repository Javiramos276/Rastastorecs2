from django.contrib import admin
from django.urls import path
from .views import view_compras, agregar_producto, eliminar_producto,tienda
from . import views

urlpatterns = [
    path('agregar/<int:arma_id>/', views.agregar_producto,name='agregar'),
    path('quitar/<int:arma_id>/', views.eliminar_producto, name='quitar'),
    path('limpiar/',views.limpiar_carrito,name='limpiar'),
    path('tienda',views.tienda,name='tienda')
]