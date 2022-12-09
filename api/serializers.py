from rest_framework import serializers
from django.core.exceptions import ValidationError

class BaseRequestSerializer(serializers.Serializer):
    callType = serializers.IntegerField(min_value= 1, max_value= 6)

class ServiceOneSerializer(serializers.Serializer):
    callType = serializers.IntegerField(min_value= 1, max_value= 6)
    userMail = serializers.CharField(max_length=50)
    userCountryCode = serializers.CharField(max_length=2)
    userLanguage = serializers.CharField(max_length=2)
    userPresenterId = serializers.IntegerField(required=False, max_value=15)

class ServiceTwoSerializer(serializers.Serializer):
    callType = serializers.IntegerField(min_value= 1, max_value= 6)
    userProg = serializers.IntegerField(max_value=15)
    userMail = serializers.CharField(max_length=50)
    userLanguage = serializers.CharField(max_length=2)
    mailVerificationCode = serializers.CharField(max_length=16)

class ServiceThreeSerializer(serializers.Serializer):
    callType = serializers.IntegerField(min_value= 1, max_value= 6)
    userProg = serializers.IntegerField(max_value=15)
    userMail = serializers.CharField(max_length=50)
    name = serializers.CharField(max_length=30)
    surname = serializers.CharField(max_length=30)
    phonePrefix = serializers.CharField(max_length=7)
    userLanguage = serializers.CharField(max_length=2)
    phoneNumber = serializers.DecimalField(max_digits=20, decimal_places=2)

class ServiceFourSerializer(serializers.Serializer):
    callType = serializers.IntegerField(min_value= 1, max_value= 6)
    userProg = serializers.IntegerField(max_value=15)
    userMail = serializers.CharField(max_length=50)
    userLanguage = serializers.CharField(max_length=2)
    phoneVerificationCode = serializers.CharField(max_length=16)

class ServiceFiveSerializer(serializers.Serializer):
    callType = serializers.IntegerField(min_value= 1, max_value= 6)
    userProg = serializers.IntegerField(max_value=15)
    userMail = serializers.CharField(max_length=50)
    userName = serializers.CharField(max_length=3)
    regAcceptTermsCondition = serializers.CharField(max_length=1)
    regAcceptPrivacy = serializers.CharField(max_length=1)
    regAcceptStatistics = serializers.CharField(max_length=1)
    appCode = serializers.CharField(max_length=3)
    appAcceptTermsCondition = serializers.CharField(required=False, max_length=1)
    appAcceptPrivacy = serializers.CharField(required=False, max_length=1)
    appAcceptStatistics = serializers.CharField(required=False, max_length=1)
    userLanguage = serializers.CharField(max_length=2)
    password = serializers.CharField(max_length=16)

class ServiceSixSerializer(serializers.Serializer):
    callType = serializers.IntegerField(min_value= 1, max_value= 6)
    userProg = serializers.IntegerField(max_value=15)
    userMail = serializers.CharField(max_length=50)
    userLanguage = serializers.CharField(max_length=2)
    promoCode = serializers.CharField(required=False, max_length=10)
    
    
    

    