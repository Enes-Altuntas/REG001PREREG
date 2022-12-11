from rest_framework import serializers
from .models import UserModel, CountryModel

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ("__all__")
        
class CountryCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CountryModel
        fields = ("__all__")