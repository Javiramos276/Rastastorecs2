from rest_framework import serializers
from .models import Arma

class ArmaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Arma
        fields='__all__'
        