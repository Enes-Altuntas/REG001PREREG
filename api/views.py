from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .serializers import *
from user.models import UserModel


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
        dbModel = UserModel.objects.get()
        if dbModel.userMail == serviceOneSerializer.data["userMail"] and dbModel.userStatus >= 4:
            return Response({"errId": 3, "errMessage": "Mail already exists"}, status=status.HTTP_400_BAD_REQUEST)

        elif dbModel.userMail == serviceOneSerializer.data["userMail"] and dbModel.userStatus < 4:
            return Response({"errId": 4, "errMessage": "Mail already exists"}, status=status.HTTP_400_BAD_REQUEST)

        # Country Table
        elif dbModel.userCountryCode != serviceOneSerializer.data["userCountryCode"]:
            return Response({"errId": 5, "errMessage": "Country code already exists"}, status=status.HTTP_400_BAD_REQUEST)
        elif request.data["UserPresenterId"] != dbModel.userPresenterId:
            dbModel.userPresenterId = request.data["UserPresenterId"]
        elif request.data["UserPresenterId"] == dbModel.userPresenterId:
            dbModel.userPresenterId = request.data["UserPresenterId"]
            return Response({"errId": 6, "errMessage": "Presenter id already exists"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            dbModel.save()
            return Response({"Success"}, status=status.HTTP_200_OK)
        except:
            return Response({"errId": 8, "errMessage": "Database error"}, status=status.HTTP_400_BAD_REQUEST)


def serviceTwo(request):
    serviceTwoSerializer = ServiceTwoSerializer(data=request.data)

    if serviceTwoSerializer.is_valid() == False:
        return Response({"errId": 1, "errMessage": serviceTwoSerializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    return None


def serviceThree(request):
    serviceThreeSerializer = ServiceThreeSerializer(data=request.data)

    if serviceThreeSerializer.is_valid() == False:
        return Response({"errId": 1, "errMessage": serviceThreeSerializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    return None


def serviceFour(request):
    serviceFourSerializer = ServiceFourSerializer(data=request.data)

    if serviceFourSerializer.is_valid() == False:
        return Response({"errId": 1, "errMessage": serviceFourSerializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    return None


def serviceFive(request):
    serviceFiveSerializer = ServiceFiveSerializer(data=request.data)

    if serviceFiveSerializer.is_valid() == False:
        return Response({"errId": 1, "errMessage": serviceFiveSerializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    return None


def serviceSix(request):
    serviceSixSerializer = ServiceSixSerializer(data=request.data)

    if serviceSixSerializer.is_valid() == False:
        return Response({"errId": 1, "errMessage": serviceSixSerializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    return None
