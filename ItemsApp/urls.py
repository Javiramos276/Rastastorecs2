from django.urls import path
from .views import ItemsView, FiltrarArmasListView


urlpatterns = [
    path("", ItemsView.as_view(), name='home'),
    path('filtrar/', FiltrarArmasListView.as_view(), name='filtrar_armas'),
    path('filtrar/<str:categoria>/', FiltrarArmasListView.as_view(), name='filtrar_armas'),
]
