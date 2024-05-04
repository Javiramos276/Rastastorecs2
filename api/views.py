from rest_framework import viewsets
from .serializer import ArmaSerializer
from .models import Arma
# Create your views here.

class ArmaViewSet(viewsets.ModelViewSet):
    queryset = Arma.objects.all()
    serializer_class = ArmaSerializer
