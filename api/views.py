from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action, api_view
from rest_framework.permissions import IsAdminUser, AllowAny,IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.generics import ListAPIView,UpdateAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.shortcuts import get_object_or_404
from .serializer import ArmaSerializer,CustomTokenObtainPairSerializer, CustomUserSerializer,CustomLoginSerializer,CustomRegisterSerializer,CarritoSerializer
from .models import Arma
from carrito.models import Carrito,Compra
from Usuarios.models import CustomUser


# Create your views here.
class ArmaViewSet(viewsets.ModelViewSet):
    queryset = Arma.objects.all()
    serializer_class = ArmaSerializer
    permission_classes = [AllowAny]

    @action(detail=False, methods=['get'],permission_classes=[IsAdminUser])
    def admin_weapons(self,request):
        armas_sin_precio = Arma.objects.filter(precio=0).values()
        serializer = self.get_serializer(armas_sin_precio, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def pistolas(self,request):
        weapon_type = ['Desert Eagle','P250','USP-S','Glock-18','Tec-9']
        armas= Arma.objects.all().filter(weapon_type__in=weapon_type).exclude(precio=0)
        serializer = self.get_serializer(armas, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['patch','get'], permission_classes=[IsAdminUser]) #el detail true agrega un id a la ruta raiz. en este caso /armas/{id}
    def modificar_arma(self,request,pk=None):
        arma = self.get_object()
        data = request.data #Esta data es la data que se le pasaria en el body desde el front. Forma 1
        
        # arma.carrito = data.get("carrito", arma.carrito) #Esto lo que hace es verificar si la informacion que yo estoy mandando tiene una clave llamada "carrito", en caso contrario retorna el valor existente de dicho campo. Esto sería la forma 1

        arma.save()
        serializer = ArmaSerializer(arma)

        return Response(serializer.data)
    



class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class CustomLoginView(APIView):
    serializer_class = CustomLoginSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True): #Verificamos si la informacion que enviamos en nuestro request es valida instanciando la clase serializadora
        
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)
            
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': user.email,
            }, status=status.HTTP_200_OK)
        
class CustomRegisterView(APIView):
    serializer_class = CustomRegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
        
            user = serializer.save(request)
            
            return Response({
                'user': user.email,
            }, status=status.HTTP_200_OK)            


class CarritoViewSet(viewsets.ModelViewSet):
    queryset = Carrito.objects.all()
    serializer_class = CarritoSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def listar(self, request):
        user = request.user
        carrito, created = Carrito.objects.get_or_create(usuario=user)
        data = carrito.obtener_carrito()
        armas_serializer = ArmaSerializer(data['armas'], many=True)
        response_data = {
            'armas': armas_serializer.data,
            'total': data['total']
        }
        return Response(response_data)

    @action(detail=False, methods=['patch'])
    def agregar_arma(self, request):
        user = request.user
        carrito, created = Carrito.objects.get_or_create(usuario=user)
        arma_id = request.data.get('arma_id') #Este request.data.get es el que le estoy pasando en la solicitud, en el body de mi peticion en POSTMAN (o react)
        arma = get_object_or_404(Arma,id=arma_id)
        carrito.agregar(arma)
        data = carrito.obtener_carrito()
        armas_serializer = ArmaSerializer(data['armas'], many=True)
        response_data = {
            'armas': armas_serializer.data,
            'total': data['total']
        }
        return Response(response_data)

    @action(detail=False, methods=['patch'])
    def eliminar_arma(self, request):
        user = request.user
        carrito = get_object_or_404(Carrito, usuario=user)
        arma_id = request.data.get('arma_id')
        arma = get_object_or_404(Arma,id=arma_id)
        carrito.eliminar(arma)
        data = carrito.obtener_carrito()
        armas_serializer = ArmaSerializer(data['armas'], many=True)
        response_data = {
            'armas': armas_serializer.data,
            'total': data['total']
        }
        return Response(response_data)

    @action(detail=False, methods=['delete'])
    def limpiar_carrito(self, request):
        user = request.user
        carrito = get_object_or_404(Carrito, usuario=user)
        armas = carrito.armas.all()
        carrito.limpiar(armas) 
        data = carrito.obtener_carrito()
        armas_serializer = ArmaSerializer(data['armas'], many=True)
        response_data = {
            'armas': armas_serializer.data,
            'total': data['total']
        }
        return Response(response_data)
        
    @action(detail=False, methods=['post'])
    def realizar_compra(self,request):
        user = request.user
        carrito = get_object_or_404(Carrito, usuario=user)
        compra = Compra(usuario=user)
        resultado = compra.verificar_objetos(carrito.armas.all())  #Aca le estoy pasando al método verificar_objetos todos las armas que estan en el carrito (es un queryset)
        if resultado['status'] == 'Exitoso':
            carrito.limpiar(carrito.armas.all())
            return Response({'mensaje': resultado}, status=status.HTTP_200_OK)
        else:
            return Response({'mensaje': resultado}, status=status.HTTP_400_BAD_REQUEST)
        