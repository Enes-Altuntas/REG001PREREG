from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .serializers import *
from user.models import UserModel, CountryModel, UserApp, VerificationCodeModel, PasswordModel, errorCodes, CustomerModel, CompanyModel, ExpertModel
from user.serializers import CountryCodeSerializer, UserSerializer, UserAppSerializer
from datetime import datetime


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
        return Response({"errId": errorCodes["errorCode"], "errMessage": errorCodes["description"]}, status=status.HTTP_400_BAD_REQUEST)

# LOGIC


def serviceOne(request):
    serviceOneSerializer = ServiceOneSerializer(data=request.data)
    if serviceOneSerializer.is_valid() == False:
        return Response({"errId": 2, "errMessage": serviceOneSerializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    if serviceOneSerializer.data["userMail"] == UserModel.objects.get(userMail=serviceOneSerializer.data["userMail"]):
        dbModel = UserModel.objects.get(
            userMail=serviceOneSerializer.data["userMail"])
        if dbModel.userStatus >= 4:
            return Response({"errId": 3, "errMessage": "Mail already exists"}, status=status.HTTP_400_BAD_REQUEST)
        elif dbModel.userStatus < 4:
            return Response({"errId": 4, "errMessage": "Mail already exists"}, status=status.HTTP_400_BAD_REQUEST)

    dbModel_CountryCode = CountryModel.objects.get(
        value=serviceOneSerializer.data["userCountryCode"])
    if dbModel_CountryCode.value != serviceOneSerializer.data["userCountryCode"]:
        return Response({"errId": 5, "errMessage": "Country code already exists"}, status=status.HTTP_400_BAD_REQUEST)
    dbModel = UserModel.objects.get()
    if CountryModel.objects.filter(value=serviceOneSerializer.data["userCountryCode"]).exists() == True:
        if serviceOneSerializer.data["userPresenterId"] != UserModel.objects.get(userPresenterId=serviceOneSerializer.data["userPresenterId"]).userPresenterId:
            return Response({"errId": 6, "errMessage": "GEN001ERR"}, status=status.HTTP_400_BAD_REQUEST)
    try:
        dbModel.userStatus = 1
        dbModel.userMail = serviceOneSerializer.data["userMail"]
        dbModel.userCountryCode = serviceOneSerializer.data["userCountryCode"]
        dbModel.userPresenterId = serviceOneSerializer.data["userPresenterId"]
        dbModel.userLanguage = serviceOneSerializer.data["userLanguage"]
        dbModel.save()
    except:
        return Response({"errId": 8, "errMessage": "DB Error"}, status=status.HTTP_400_BAD_REQUEST)
    # BEFORE SENDING THE VERIFICATION SERVICE WE NEED TO GET HIS PHONE NUMBER SO MY IDEA IS A COMPLETE REGISTRATION PAGE THAT WE COLLECT ALL THE DATA OTHERWISE
    # THAT SUBSERVICE IS NOT GOING TO WORK UNDER SERVICE ONE WE NEED TO CREATE ANOTHER CALLTYPE TO CALL THE SERVICE

    # -------------------------------------------------------------------------------------------------------------

    # CHECK USER_USERTYPE
    if serviceOneSerializer.data["userType"] == "CU":
        customer = CustomerModel.objects.get(
            cus_mail=serviceOneSerializer.data["userMail"])
        try:
            customer.cus_prog = serviceOneSerializer.data["userProg"]
            customer.save()
        except:
            return Response({"errId": 8, "errMessage": "DB Error"}, status=status.HTTP_400_BAD_REQUEST)
    if serviceOneSerializer.data["userType"] == "CO":
        company = CompanyModel.objects.get(
            comp_mail=serviceOneSerializer.data["userMail"])
        try:
            company.comp_prog = serviceOneSerializer.data["userProg"]
            company.save()
        except:
            return Response({"errId": 8, "errMessage": "DB Error"}, status=status.HTTP_400_BAD_REQUEST)
    if serviceOneSerializer.data["userType"] == "EX":
        expert = ExpertModel.objects.get(
            exp_mail=serviceOneSerializer.data["userMail"])
        try:
            expert.exp_prog = serviceOneSerializer.data["userProg"]
            expert.save()
        except:
            return Response({"errId": 8, "errMessage": "DB Error"}, status=status.HTTP_400_BAD_REQUEST)

    if REG007SENDVERCODE(serviceOneSerializer.data) is False:
        return Response({"errId": 7, "errMessage": "GEN001ERR"}, status=status.HTTP_400_BAD_REQUEST)

    return Response({"Success"}, status=status.HTTP_200_OK)


def serviceTwo(request):
    serviceTwoSerializer = ServiceTwoSerializer(data=request.data)
    if serviceTwoSerializer.is_valid() == False:
        return Response({"errId": 2, "errMessage": serviceTwoSerializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    try:
        dbModel = UserModel.objects.get(
            userMail=serviceTwoSerializer.data["userMail"])
    except:
        return Response({"errId": 9, "errMessage": "Mail not found"}, status=status.HTTP_400_BAD_REQUEST)
    if REG007SENDVERCODE(serviceTwoSerializer.data) is False:
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
    if serviceThreeSerializer.is_valid() == False:
        return Response({"errId": 1, "errMessage": serviceThreeSerializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    try:
        dbModel = UserModel.objects.get(
            userMail=serviceThreeSerializer.data["userMail"])
    except:
        return Response({"errId": 9, "errMessage": "Mail not found"}, status=status.HTTP_400_BAD_REQUEST)
    if dbModel.userMail != serviceThreeSerializer.data["userMail"]:
        return Response({"errId": 2, "errMessage": serviceThreeSerializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    try:
        dbModel.userStatus = 3
        dbModel.name = serviceThreeSerializer.data["name"]
        dbModel.surname = serviceThreeSerializer.data["surname"]
        dbModel.phoneNumber = serviceThreeSerializer.data["phoneNumber"]
        dbModel.phonePrefix = serviceThreeSerializer.data["phonePrefix"]
        dbModel.save()
    except:
        return Response({"errId": 10, "errMessage": "Database error"}, status=status.HTTP_400_BAD_REQUEST)

    if REG007SENDVERCODE(serviceThreeSerializer.data) is False:
        return Response({"errId": 12, "errMessage": "GEN001ERR"}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"Success"}, status=status.HTTP_200_OK)


def serviceFour(request):
    serviceFourSerializer = ServiceFourSerializer(data=request.data)
    if serviceFourSerializer.is_valid() == False:
        return Response({"errId": 2, "errMessage": serviceFourSerializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    try:
        dbModel = UserModel.objects.get(
            userMail=serviceFourSerializer.data["userMail"])
    except:
        return Response({"errId": 9, "errMessage": "Mail not found"}, status=status.HTTP_400_BAD_REQUEST)
    if REG008CHECKVERCODE(serviceFourSerializer.data) is False:
        return Response({"errId": 27, "errMessage": "GEN001ERR"}, status=status.HTTP_400_BAD_REQUEST)
    else:
        try:
            dbModel.userStatus = 4
            dbModel.save()
            return Response({"Success"}, status=status.HTTP_200_OK)
        except:
            return Response({"errId": 10, "errMessage": "Database error"}, status=status.HTTP_400_BAD_REQUEST)


def serviceFive(request):
    serviceFiveSerializer = ServiceFiveSerializer(data=request.data)
    if serviceFiveSerializer.is_valid() == False:
        return Response({"errId": 2, "errMessage": serviceFiveSerializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    try:
        dbModel = UserModel.objects.get(
            userMail=serviceFiveSerializer.data["userMail"])
    except:
        return Response({"errId": 9, "errMessage": "Mail not found"}, status=status.HTTP_400_BAD_REQUEST)
    dbModel_app = UserApp.objects.get()
    if dbModel_app.appID != int(serviceFiveSerializer.data["appID"]):
        return Response({"errId": 13, "errMessage": serviceFiveSerializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    if REG002PSWMNG(serviceFiveSerializer.data) is False:
        return Response({"errId": 14, "errMessage": "GEN001ERR"}, status=status.HTTP_400_BAD_REQUEST)
    try:
        dbModel.userStatus = 5
        dbModel.userName = serviceFiveSerializer.data["userName"]
        dbModel.acceptPrivacy = serviceFiveSerializer.data["regAcceptPrivacy"]
        dbModel.acceptTermsCondition = serviceFiveSerializer.data["regAcceptTermsCondition"]
        dbModel.acceptStatistics = serviceFiveSerializer.data["regAcceptStatistics"]
        dbModel.save()
    except:
        return Response({"errId": 10, "errMessage": "Database error"}, status=status.HTTP_400_BAD_REQUEST)
    try:
        dbModel_app.appID = serviceFiveSerializer.data["appID"]
        dbModel_app.userProgress = serviceFiveSerializer.data["userProg"]
        dbModel_app.userStatus = 5
        return Response({"Success"}, status=status.HTTP_200_OK)
    except:
        return Response({"errId": 8, "errMessage": "Database error"}, status=status.HTTP_400_BAD_REQUEST)


def serviceSix(request):
    serviceSixSerializer = ServiceSixSerializer(data=request.data)
    dbModel = UserModel.objects.get(
        userMail=serviceSixSerializer.data["userMail"])
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
        dbModel.userID = serviceSixSerializer.data["promoCode"]
        dbModel.save()
        return Response({"Success"}, status=status.HTTP_200_OK)
    except:
        return Response({"errId": 10, "errMessage": "Database error"}, status=status.HTTP_400_BAD_REQUEST)


def REG009LOGIN(request):
    loginSerializer = LoginSerializer(data=request.data)
    dbModel = UserModel.objects.get(userProg=loginSerializer.data["userProg"])
    if loginSerializer.is_valid() == False:
        return Response({"errId": 1, "errMessage": loginSerializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    if loginSerializer["prog"].is_Present():
        if (loginSerializer["prog"] != dbModel.userProg):
            return Response({"errId": 30, "errMessage": "GEN001ERR"}, status=status.HTTP_400_BAD_REQUEST)
        loginSerializer.data["functionType"] = "V"
        REG002PSWMNG(loginSerializer.data)


def REG007SENDVERCODE(request):
    user = UserModel.objects.get(userMail=request["userMail"])
    is_Active = True
    verificationCode = SendVerCodeSerializer(data=request)
    if verificationCode.is_valid() == False:
        verification = VerificationCodeModel.objects.get(
            verUserProg=verificationCode.data["userProg"])
        if verificationCode.userProg != user.userProg:
            return Response({"errId": 2, "errMessage": "GEN001ERR"}, status=status.HTTP_400_BAD_REQUEST)
        # how to check verification code already exist
        # max start date?
        if verificationCode.data["user_prog"] != user.userProg and verification.verStartDate != 9999999:
            is_Active = False
            return Response({"errId": 1, "errMessage": "GEN001ERR", "active": is_Active}, status=status.HTTP_400_BAD_REQUEST)
        # generate verification code?


def REG002PSWMNG(userData):
    user = UserModel.objects.get(userProg=userData["userProg"])
    password = PasswordModel.objects.get(passwordUserProg=userData["userProg"])
    passwordCheck = ServiceFiveSerializer(data=userData.data)
    if passwordCheck.is_valid():
        if "I" == passwordCheck.data["userFunctionType"]:
            if passwordCheck.data["userProg"] != user.data["userProg"]:
                return Response({"errId": 2, "errMessage": "GEN001ERR"}, status=status.HTTP_400_BAD_REQUEST)
            if passwordCheck.data["userPassword"] != password.passwordPassword:
                return Response({"errId": 17, "errMessage": "GEN001ERR"}, status=status.HTTP_400_BAD_REQUEST)
            if passwordCheck.data["userPassword"].length < 8 and type(passwordCheck.data["userPassword"]) == int:
                return Response({"errId": 18, "errMessage": "GEN001ERR"}, status=status.HTTP_400_BAD_REQUEST)
            try:
                password.passwordPassword = passwordCheck.data["userPassword"]
                password.passwordStatus = "A"
                password.passwordUserProg = passwordCheck.data["userProg"]
                password.passwordLastLogin = datetime.now()
                password.passwordStartDate = datetime.now()
                password.passwordEndDate = 999999999
                password.save()
                return Response({"Success"}, status=status.HTTP_200_OK)
            except:
                return Response({"errId": 8, "errMessage": "Database error"}, status=status.HTTP_400_BAD_REQUEST)
        elif "C" == passwordCheck.data["userFunctionType"]:
            if passwordCheck.is_valid():
                if passwordCheck.data["oldPassword"] != password.passwordPassword and password.passwordStatus != "A":
                    return Response({"errId": 19, "errMessage": "GEN001ERR"}, status=status.HTTP_400_BAD_REQUEST)
                if passwordCheck.data["newPassword"] == password.passwordPassword:
                    return Response({"errId": 20, "errMessage": "GEN001ERR"}, status=status.HTTP_400_BAD_REQUEST)
                if passwordCheck.data["newPassword"].length == 8 and type(passwordCheck.data["newPassword"]) == int:
                    try:
                        password.passwordPassword = passwordCheck.data["newPassword"]
                        password.passwordStatus = "E"
                        password.save()
                    except:
                        return Response({"errId": 8, "errMessage": "Database error"}, status=status.HTTP_400_BAD_REQUEST)
                try:
                    password.passwordPassword = passwordCheck.data["newPassword"]
                    password.passwordStatus = "A"
                    password.passwordUserProg = passwordCheck.data["userProg"]
                    password.passwordLastLogin = datetime.now()
                    password.passwordStartDate = datetime.now()
                    password.passwordEndDate = 999999999
                    password.save()
                    return Response({"Success"}, status=status.HTTP_200_OK)
                except:
                    return Response({"errId": 8, "errMessage": "Database error"}, status=status.HTTP_400_BAD_REQUEST)
        elif "V" == passwordCheck.data["userFunctionType"]:
            # check for each input type
            if passwordCheck.data["userProg"] != user.data["userProg"] and password.passwordStartDate != password.passwordStartDate:
                return Response({"errId": 20, "errMessage": "GEN001ERR"}, status=status.HTTP_400_BAD_REQUEST)
            if password.passwordCterr == 5 and password.passwordStatus == "L":
                try:
                    password.passwordLastLogin = datetime.now()
                    password.passwordStatus = "L"
                    password.save()
                    return Response({"errId": 22, "errMessage": "GEN001ERR"}, status=status.HTTP_400_BAD_REQUEST)
                except:
                    return Response({"errId": 10, "errMessage": "Database error"}, status=status.HTTP_400_BAD_REQUEST)
            if datetime.now().minute > password.passwordEndDate and password.passwordStatus == "E":
                try:
                    password.passwordStatus = "E"
                    password.passwordLastLogin = datetime.now()
                    password.save()
                    return Response({"errId": 21, "errMessage": "GEN001ERR"}, status=status.HTTP_400_BAD_REQUEST)
                except:
                    return Response({"errId": 10, "errMessage": "Database error"}, status=status.HTTP_400_BAD_REQUEST)
            if passwordCheck.data["userPassword"] == password.passwordPassword:
                try:
                    password.passwordCterr = password.passwordCterr + 1
                    password.passwordLastLogin = datetime.now()
                    password.save()
                    return Response({"errId": 20, "errMessage": "GEN001ERR"}, status=status.HTTP_400_BAD_REQUEST)
                except:
                    return Response({"errId": 10, "errMessage": "Database error"}, status=status.HTTP_400_BAD_REQUEST)
            try:
                password.passwordLastLogin = datetime.now()
                password.save()
            except:
                return Response({"errId": 10, "errMessage": "GEN001ERR"}, status=status.HTTP_400_BAD_REQUEST)


def REG012CHKPROMO(userData):
    return True


def REG011IDCREATION(userData):
    dbModel = UserModel.objects.get()
    dbModel.userID = userData["countryCode"] + userData["userProg"]

    return dbModel.userProg


def REG008CHECKVERCODE(userData):
    subService = subServiceOne(data=userData)
    if subService.is_valid():
        if not "M" or "P" or "W" in subService.data["userFunctionType"]:
            return Response({"errId": 1, "errMessage": "GEN001ERR"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"errId": 2, "errMessage": "GEN001ERR"}, status=status.HTTP_400_BAD_REQUEST)
    verification = VerificationCodeModel.objects.get(
        verUserProg=subService.data["userProg"])
    if subService.data["userProg"] != verification.verUserProg and verification.verStartDate != verification.verStartDate:
        return Response({"errId": 23, "errMessage": "GEN001ERR"}, status=status.HTTP_400_BAD_REQUEST)
    if subService.initial_data["mailVerificationCode"] != verification.verificationCode:
        return Response({"errId": 23, "errMessage": "GEN001ERR"}, status=status.HTTP_400_BAD_REQUEST)
    if verification.cterr != 5 and verification.status == "L":
        try:
            verification.status = "L"
            verification.lastLoginerr = datetime.now()
            verification.save()
            return Response({"errId": 24, "errMessage": "GEN001ERR"}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"errId": 10, "errMessage": "Database error"}, status=status.HTTP_400_BAD_REQUEST)
    if datetime.now().minute < verification.verEndDate.minute:
        try:
            verification.status = "E"
            verification.lastLoginerr = datetime.now()
            verification.save()
            # return Response({"errId": 25, "errMessage": "GEN001ERR"}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"errId": 10, "errMessage": "Database error"}, status=status.HTTP_400_BAD_REQUEST)
    verification.status = "A"
    if verification.status == "E":
        return Response({"errId": 25, "errMessage": "GEN001ERR"}, status=status.HTTP_400_BAD_REQUEST)
    if verification.status == "L":
        return Response({"errId": 23, "errMessage": "GEN001ERR"}, status=status.HTTP_400_BAD_REQUEST)
    if verification.status == "A":
        try:
            verification.lasttentative = datetime.now()
            verification.save()
        except:
            return Response({"errId": 10, "errMessage": "Database error"}, status=status.HTTP_400_BAD_REQUEST)
