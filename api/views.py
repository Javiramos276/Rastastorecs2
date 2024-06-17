from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action, api_view
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from django.shortcuts import get_object_or_404
from .serializer import ArmaSerializer,CustomTokenObtainPairSerializer, CustomUserSerializer,CustomLoginSerializer
from .models import Arma
from Usuarios.models import CustomUser


# Create your views here.
class ArmaViewSet(viewsets.ModelViewSet):
    queryset = Arma.objects.all()
    serializer_class = ArmaSerializer
    permission_classes = [AllowAny]

    @action(detail=False, methods=['get'], permission_classes=[IsAdminUser])
    def admin_weapons(self, request):
        armas_sin_precio = Arma.objects.filter(precio=0).values()
        serializer = self.get_serializer(armas_sin_precio, many=True)
        return Response(serializer.data)

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class CustomLoginView(APIView):
    serializer_class = CustomLoginSerializer

