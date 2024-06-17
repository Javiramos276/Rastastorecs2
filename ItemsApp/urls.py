from django.urls import path
from .views import view_home,view_cargar_objetos,nav_bar,view_pistolas_filter,view_rifles_filter,view_factorynew_filter,view_agregar_precio,view_eliminar_item,view_get_precios



urlpatterns = [
    path('cargar_items/',view_cargar_objetos,name='cargar_items'),
    path('ver_items',view_home, name='items'),
    path('nav_bar',nav_bar, name='nav'),
    path('pistolas/',view_pistolas_filter,name='pistolas'),
    path('rifles/',view_rifles_filter,name='rifles'),
    path('estado/factory_new', view_factorynew_filter, name='factorynew'),
    path('actualizar_precio/<int:arma_id>/',view_agregar_precio,name='agregar_precio'),
    path('delete_item/<int:arma_id>/',view_eliminar_item,name='borrar_item'),
    path('get_precios/',view_get_precios, name='get_precios'),
]
