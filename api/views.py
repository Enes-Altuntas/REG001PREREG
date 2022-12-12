from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .serializers import *
from user.models import UserModel ,CountryModel,UserApp
from user import serializers


@api_view(['POST'])
def mainService(request):
    baseSerializer = BaseRequestSerializer(data=request.data)

    if baseSerializer.is_valid():
        if baseSerializer.data["callType"] == 1:
            return serviceOne(request)
        elif baseSerializer.data["callType"] == 2:
            return serviceTwo(request)
        elif baseSerializer.data["callType"] == 3:
            return serviceThree(request)
        elif baseSerializer.data["callType"] == 4:
            return serviceFour(request)
        elif baseSerializer.data["callType"] == 5:
            return serviceFive(request)
        elif baseSerializer.data["callType"] == 6:
            return serviceSix(request)
    else:
        return Response({"errId": 1, "errMessage": baseSerializer.errors}, status=status.HTTP_400_BAD_REQUEST)


def serviceOne(request):
    serviceOneSerializer = ServiceOneSerializer(data=request.data)
    if serviceOneSerializer.is_valid() == False:
        return Response({"errId": 2, "errMessage": serviceOneSerializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    else:
        try:
            dbModel_CountryCode = CountryModel.objects.get(countryCode=serviceOneSerializer.data["value"])
            dbModel = UserModel.objects.get(userMail=serviceOneSerializer.data["userMail"])
        except:        
            if dbModel.userMail == serviceOneSerializer.data["userMail"]:
                if dbModel.userStatus >= 4:
                    return Response({"errId": 3, "errMessage": "Mail already exists"}, status=status.HTTP_400_BAD_REQUEST)
                elif dbModel.userStatus < 4:
                    return Response({"errId": 4, "errMessage": "Mail already exists"}, status=status.HTTP_400_BAD_REQUEST)            

        if dbModel_CountryCode.userCountryCode != serviceOneSerializer.data["userCountryCode"]:
            return Response({"errId": 5, "errMessage": "Country code already exists"}, status=status.HTTP_400_BAD_REQUEST)
        
        if dbModel.userPresenterId is not None:
            if serviceOneSerializer.data["userPresenterId"] != dbModel.userPresenterId:
                return Response({"errId": 6, "errMessage": "GEN001ERR"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            countryCodeSerializer = serializers.CountryModelSerializer(data=request.data)
            userSerializer = serializers.UserSerializer(data=request.data)
            if userSerializer.is_valid() and countryCodeSerializer.is_valid():
                countryCodeSerializer.save()
                userSerializer.save()
        except:
           return Response({"errId": 8, "errMessage": "DB Error"}, status=status.HTTP_400_BAD_REQUEST)
       
        if REG007SENDVERCODE(userSerializer.data) is False:
            return Response({"errId": 7, "errMessage": "GEN001ERR"}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({"Success"}, status=status.HTTP_200_OK)
                

def serviceTwo(request):
    serviceTwoSerializer = ServiceTwoSerializer(data=request.data)

    if serviceTwoSerializer.is_valid() == False:
        return Response({"errId": 2, "errMessage": serviceTwoSerializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    else:
        dbModel = UserModel.objects.get()
        if dbModel.userMail != serviceTwoSerializer.data["userMail"]:
            return Response({"errId": 9, "errMessage": "Incorrect Mail"}, status=status.HTTP_400_BAD_REQUEST)
        
        #ANOTHER SERVICE
    if REG008SENDVERCODE(serviceTwoSerializer.data) is False:
            return Response({"errId": 27, "errMessage": "GEN001ERR"}, status=status.HTTP_400_BAD_REQUEST)
        
        
    try:
        #dbModel.objects.get(UserModel.userStatus == 2)
        dbModel.userStatus = 2
        dbModel.save()
        return Response({"Success"}, status=status.HTTP_200_OK)
    except:
            return Response({"errId": 10, "errMessage": "Database error"}, status=status.HTTP_400_BAD_REQUEST)
            

def serviceThree(request):
    serviceThreeSerializer = ServiceThreeSerializer(data=request.data)
    dbModel = UserModel.objects.get()
    if serviceThreeSerializer.is_valid() == False:
        return Response({"errId": 1, "errMessage": serviceThreeSerializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    else:
        if dbModel.userMail != serviceThreeSerializer.data["userMail"]:
            return Response({"errId": 2, "errMessage": serviceThreeSerializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                dbModel.userStatus = 3
                dbModel.name = serviceThreeSerializer.data["name"]
                dbModel.surname = serviceThreeSerializer.data["surname"]
                dbModel.phoneNumber =  serviceThreeSerializer.data["phoneNumber"]
                dbModel.phonePrefix =   serviceThreeSerializer.data["phonePrefix"]
                dbModel.save()
                
            except:
                return Response({"errId": 10, "errMessage": "Database error"}, status=status.HTTP_400_BAD_REQUEST)
            
            if REG007SENDVERCODE(serviceThreeSerializer.data) is False:
                return Response({"errId": 12, "errMessage": "GEN001ERR"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"Success"}, status=status.HTTP_200_OK)


def serviceFour(request):
    serviceFourSerializer = ServiceFourSerializer(data=request.data)
    dbModel = UserModel.objects.get()
    if serviceFourSerializer.is_valid() == False:
        return Response({"errId": 2, "errMessage": serviceFourSerializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    if dbModel.userMail != serviceFourSerializer.data["userMail"]:
            return Response({"errId": 9, "errMessage": serviceFourSerializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    if REG008SENDVERCODE(serviceFourSerializer.data) is False:
            return Response({"errId": 27, "errMessage": "GEN001ERR"}, status=status.HTTP_400_BAD_REQUEST)
    else:
        try:
            dbModel.userStatus = 4
            dbModel.save()
            return Response({"Success"}, status=status.HTTP_200_OK)
        except:
            return Response({"errId": 10, "errMessage": "Database error"}, status=status.HTTP_400_BAD_REQUEST)
            
        
        
    return None


def serviceFive(request):
    serviceFiveSerializer = ServiceFiveSerializer(data=request.data)
    dbModel = UserModel.objects.get()
    dbModel_app = UserApp.objects.get()
    if serviceFiveSerializer.is_valid() == False:
        return Response({"errId": 2, "errMessage": serviceFiveSerializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    if dbModel.userMail != serviceFiveSerializer.data["userMail"]:
            return Response({"errId": 9, "errMessage": serviceFiveSerializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    if dbModel_app.appID != serviceFiveSerializer.data["appID"]:
            return Response({"errId": 13, "errMessage": serviceFiveSerializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    if REG002PSWMNG(serviceFiveSerializer.data) is False:
        return Response({"errId": 14, "errMessage": "GEN001ERR"}, status=status.HTTP_400_BAD_REQUEST)
    try:
        dbModel.userStatus = 5
        dbModel.userName = serviceFiveSerializer.data["userName"]
        dbModel.acceptPrivacy = serviceFiveSerializer.data["acceptPrivacy"]
        dbModel.acceptTermsCondition = serviceFiveSerializer.data["acceptTermsConditions"]
        dbModel.acceptStatistics = serviceFiveSerializer.data["acceptStatistics"]
    except:
        return Response({"errId": 10, "errMessage": "Database error"}, status=status.HTTP_400_BAD_REQUEST)
    try:
        dbModel_app.appID = serviceFiveSerializer.data["appID"]
        dbModel_app.userProgress = serviceFiveSerializer.data["userProgress"]
        dbModel_app.userStatus = serviceFiveSerializer.data["userStatus"]
        return Response({"Success"}, status=status.HTTP_200_OK)
    except:
        return Response({"errId": 8, "errMessage": "Database error"}, status=status.HTTP_400_BAD_REQUEST)
    

def serviceSix(request):
    serviceSixSerializer = ServiceSixSerializer(data=request.data)
    dbModel = UserModel.objects.get()
    if serviceSixSerializer.is_valid() == False:
        return Response({"errId": 1, "errMessage": serviceSixSerializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    if REG012CHKPROMO(serviceSixSerializer.data) is False:
        return Response({"errId": 26, "errMessage": "GEN001ERR"}, status=status.HTTP_400_BAD_REQUEST)
    if dbModel.userMail != serviceSixSerializer.data["userMail"]:
            return Response({"errId": 9, "errMessage": serviceSixSerializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        REG011IDCREATION(serviceSixSerializer.data)
    except:
        return Response({"errId": 16, "errMessage": "GEN001ERR"}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        dbModel.promoCode = serviceSixSerializer.data["promoCode"]
        dbModel.userID = REG011IDCREATION()
        dbModel.save()
        return Response({"Success"}, status=status.HTTP_200_OK)
    except:
        return Response({"errId": 10, "errMessage": "Database error"}, status=status.HTTP_400_BAD_REQUEST)
    
    
    

    return None


def REG007SENDVERCODE(userData):
    return True

def REG008SENDVERCODE(userData):
    return True

def REG002PSWMNG(userData):
    return True

def REG012CHKPROMO(userData):
    return True

def REG011IDCREATION(userData):
    #userdata promocode => userprog
    userID = UserModel.objects.create(serviceSixSerializer.data["promoCode"])
    
    return userID