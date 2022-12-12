from rest_framework import serializers
from .models import UserModel, CountryModel,UserApp

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ("__all__")
        
class CountryCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CountryModel
        fields = ("__all__")
        
class UserAppSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserApp
        fields = ("__all__")