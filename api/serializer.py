from rest_framework import serializers,exceptions
from .models import Arma
from Usuarios.models import CustomUser
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework import status
from allauth.account.adapter import get_adapter
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import LoginSerializer
from rest_framework import serializers
from allauth.account.utils import setup_user_email

class ArmaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Arma
        fields='__all__'
        
# Creo una customizacion de mi obtencion de token porque defini mi usuario con el campo email en principio
# Informacion mas a detalle se encuentra en https://medium.com/django-unleashed/email-authentication-designing-a-modern-system-in-django-rest-framework-without-the-traditional-f2758ae08c31
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = 'email'

    def validate(self, attrs):
        credentials = {
            'email': attrs.get('email'),
            'password': attrs.get('password')
        }

        user = authenticate(**credentials)

        #Aca se chequea si existe el usuario con las credenciales que se pasa con **credentials. El ** implica que le puedo pasar un dict
        if user:
            if not user.is_active:
                raise exceptions.AuthenticationFailed('User is deactivated')

            data = {}
            refresh = self.get_token(user)

            data['refresh'] = str(refresh)
            data['access'] = str(refresh.access_token)

            return data
        else:
            raise exceptions.AuthenticationFailed('No active account found with the given credentials')
    

#Modificamos el registro de usuarios a uno personalizado porque nuestro modelo no tiene el campo username
class CustomRegisterSerializer(RegisterSerializer):
    username = None 

    def get_cleaned_data(self):
        return {
            'email': self.validated_data.get('email', ''),
            'password1': self.validated_data.get('password1', ''),
            'password2': self.validated_data.get('password2', ''),
        }
    
    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        user.email = self.cleaned_data.get('email')
        user.set_password(self.cleaned_data.get('password1'))
        user.save()
        setup_user_email(request, user, [])

class CustomLoginSerializer(LoginSerializer):
    username = None 

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        user = authenticate(username=email, password=password) #El metodo authenticate retorna un objeto usuario si las credenciales son correctas.
        if user is not None:
            print(f'Usuario validado correctamente')
            attrs['user'] = user
            return attrs
        else:
            raise serializers.ValidationError('Las credenciales no son correctas')

        


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'