from django.urls import path
from .views import view_home,view_cargar_objetos


urlpatterns = [
    path('', view_home, name='home'),
    path('cargar_items/',view_cargar_objetos,name='cargar_items')
]
