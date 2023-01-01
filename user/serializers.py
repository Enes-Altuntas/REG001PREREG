from rest_framework import serializers
from .models import UserModel, CountryModel, UserApp, VerificationCodeModel

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


class SendVerCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = VerificationCodeModel
        fields = ("__all__")
