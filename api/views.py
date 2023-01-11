from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .serializers import *
from user.models import UserModel, CountryModel, UserApp, VerificationCodeModel, PasswordModel, errorCodes, CustomerModel, CompanyModel, ExpertModel, LanguageModel
from user.serializers import CountryCodeSerializer, UserSerializer, UserAppSerializer
from datetime import datetime , timedelta


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
    if UserModel.objects.filter(userMail=serviceOneSerializer.data["userMail"]).exists() == True:
        if serviceOneSerializer.data["userMail"] == UserModel.objects.get(userMail=serviceOneSerializer.data["userMail"]):
            dbModel = UserModel.objects.get(
                userMail=serviceOneSerializer.data["userMail"])
            if dbModel.userStatus >= 4:
                return Response({"errId": 3, "errMessage": "Mail already exists"}, status=status.HTTP_400_BAD_REQUEST)
            elif dbModel.userStatus < 4:
                return Response({"errId": 4, "errMessage": "Mail already exists"}, status=status.HTTP_400_BAD_REQUEST)

    if CountryModel.objects.filter(value=serviceOneSerializer.data["userCountryCode"]).exists() == True:
        if serviceOneSerializer.data["userPresenterId"] != UserModel.objects.get(userPresenterId=serviceOneSerializer.data["userPresenterId"]).userPresenterId:
            return Response({"errId": 6, "errMessage": "GEN001ERR"}, status=status.HTTP_400_BAD_REQUEST)
    try:
        UserModel.objects.create(
            userMail=serviceOneSerializer.data["userMail"],
            userCountryCode=serviceOneSerializer.data["userCountryCode"],
            userPresenterID=serviceOneSerializer.data["userPresenterID"],
            userLanguage=serviceOneSerializer.data["userLanguage"],
            userStatus=1)
    except:
        return Response({"errId": 8, "errMessage": "DB Error"}, status=status.HTTP_400_BAD_REQUEST)

    # -------------------------------------------------------------------------------------------------------------

    # CHECK USER_USERTYPE
    if serviceOneSerializer.data["userType"] == "CU":
        try:
            CustomerModel.objects.create(
                cus_prog=serviceOneSerializer.data["userPresenterID"], cus_mail=serviceOneSerializer.data["userMail"])
        except:
            return Response({"errId": 8, "errMessage": "DB Error"}, status=status.HTTP_400_BAD_REQUEST)
    if serviceOneSerializer.data["userType"] == "CO":
        try:
            CompanyModel.objects.create(
                comp_prog=serviceOneSerializer.data["userPresenterID"], comp_mail=serviceOneSerializer.data["userMail"])
        except:
            return Response({"errId": 8, "errMessage": "DB Error"}, status=status.HTTP_400_BAD_REQUEST)
    if serviceOneSerializer.data["userType"] == "EX":
        try:
            ExpertModel.objects.create(
                exp_mail=serviceOneSerializer.data["userMail"])
        except:
            return Response({"errId": 8, "errMessage": "DB Error"}, status=status.HTTP_400_BAD_REQUEST)
    serviceOneSerializer.data["userProg"] = UserModel.objects.get(
        userMail=serviceOneSerializer.data["userMail"]).userProg
    if REG007SENDVERCODE(serviceOneSerializer.data) is False:
        return Response({"errId": 7, "errMessage": "GEN001ERR"}, status=status.HTTP_400_BAD_REQUEST)

    return Response({"Success"}, status=status.HTTP_200_OK)


def serviceTwo(request):
    serviceTwoSerializer = ServiceTwoSerializer(data=request.data)
    if serviceTwoSerializer.is_valid() == False:
        return Response({"errId": 2, "errMessage": serviceTwoSerializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    if UserModel.objects.filter(userProg=serviceTwoSerializer.data["userProg"]).exists() and UserModel.objects.get(
        userProg=serviceTwoSerializer.data["userProg"]) != serviceTwoSerializer.data["userProg"]:
        return Response ({"errId": 2, "errMessage": "GEN001ERR"}, status=status.HTTP_400_BAD_REQUEST)
    try:
        user = UserModel.objects.get(
            userMail=serviceTwoSerializer.data["userMail"])
    except:
        return Response({"errId": 9, "errMessage": "Mail not found"}, status=status.HTTP_400_BAD_REQUEST)
    if REG008CHECKVERCODE(serviceTwoSerializer.data) is False:
        return Response({"errId": 27, "errMessage": "GEN001ERR"}, status=status.HTTP_400_BAD_REQUEST)
    try:
        user.userStatus = 2
        user.save()
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
        dbModel.phoneNumber = serviceThreeSerializer.data["phoneNumber"]
        dbModel.phonePrefix = serviceThreeSerializer.data["phonePrefix"]
        dbModel.save()
    except:
        return Response({"errId": 10, "errMessage": "Database error"}, status=status.HTTP_400_BAD_REQUEST)
    if serviceThreeSerializer.data["userType"] == "CU":
        customer = CustomerModel.objects.get(
            cus_mail=serviceThreeSerializer.data["userProg"])
        try:
            customer.cus_name = serviceThreeSerializer.data["name"]
            customer.cus_surname = serviceThreeSerializer.data["surname"]
            customer.cus_prog = serviceThreeSerializer.data["userProg"]
            customer.save()
        except:
            return Response({"errId": 8, "errMessage": "DB Error"}, status=status.HTTP_400_BAD_REQUEST)
    if serviceThreeSerializer.data["userType"] == "CO":
        company = CompanyModel.objects.get(
            comp_prog=serviceThreeSerializer.data["userProg"])  # USERPROG INSTEAD OF MAIL
        try:
            company.comp_prog = serviceThreeSerializer.data["userProg"]
            company.save()
        except:
            return Response({"errId": 8, "errMessage": "DB Error"}, status=status.HTTP_400_BAD_REQUEST)
    if serviceThreeSerializer.data["userType"] == "EX":
        expert = ExpertModel.objects.get(
            exp_mail=serviceThreeSerializer.data["userProg"])
        try:
            expert.exp_prog = serviceThreeSerializer.data["userProg"]
            expert.save()
        except:
            return Response({"errId": 8, "errMessage": "DB Error"}, status=status.HTTP_400_BAD_REQUEST)

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


# def serviceSeven(request):
#     serviceSevenSerializer = ServiceSevenSerializer(data=request.data)
#     if serviceSevenSerializer.is_valid() == False:
#         return Response({"errId": 5, "errMessage": serviceSevenSerializer.errors}, status=status.HTTP_400_BAD_REQUEST)
#     try:
#         db_language = LanguageModel.objects.using('db99').get(
#             userLanguage=serviceSevenSerializer.data["userLanguage"])
#     except:
#         return Response({"errId": 2, "errMessage": serviceSevenSerializer.error_messages}, status=status.HTTP_400_BAD_REQUEST)
#     if serviceSevenSerializer.data["callType"] == "front":
#         try:
#             db_user = UserModel.objects.get(
#                 userProg=serviceSevenSerializer.data["ownerId"])
#         except:
#             return Response({"errId": 5, "errMessage": serviceSevenSerializer.error_messages}, status=status.HTTP_400_BAD_REQUEST)
#     elif serviceSevenSerializer.data["callType"] == "back":
#         db_user.userCountryCode = serviceSevenSerializer.data["userCountryCode"]
#     else:
#         return Response({"errId": 9, "errMessage": serviceSevenSerializer.error_messages}, status=status.HTTP_400_BAD_REQUEST)
#     if serviceSevenSerializer.data["presenterId"] == "":
#         db_user.userCountryCode = serviceSevenSerializer.data["userCountryCode"]
#     if serviceSevenSerializer.data["presenterId"] == serviceSevenSerializer.data["ownerId"]:
#         return Response({"errId": 8, "errMessage": serviceSevenSerializer.error_messages}, status=status.HTTP_400_BAD_REQUEST)
#     else:
#         try:
#             db_presenter = UserModel.objects.get(
#                 userProg=serviceSevenSerializer.data["presenterId"])
#         except:
#             return Response({"errId": 6, "errMessage": serviceSevenSerializer.error_messages}, status=status.HTTP_400_BAD_REQUEST)
#     if db_presenter.userStatus > 4:
#         db_presenter.userStatus = 0
#     else:
#         return Response({"errId": 7, "errMessage": serviceSevenSerializer.error_messages}, status=status.HTTP_400_BAD_REQUEST)
#     if serviceSevenSerializer.data["countryCode"] == db_user.userCountryCode:
#         db_communty = CommunityModel.objects.using('db99').get(
#             userProg=serviceSevenSerializer.data["ownerId"])
#     else:
#         return Response({"errId": 0, "errMessage": "Different Country!"}, status=status.HTTP_400_BAD_REQUEST)


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
    verificationCode = request
    try:
        verification = VerificationCodeModel.objects.get(
                verUserProg=user.userProg)
    except:
        return Response({"errId": 2, "errMessage": "GEN001ERR"}, status=status.HTTP_400_BAD_REQUEST)
    if verification.verUserProg != user.userProg:
            return False
    try:
        verStartDate = verification.verStartDate
        verUserProg = verification.verUserProg
    except:
        return Response({"errId": 1, "errMessage": "GEN001ERR"}, status=status.HTTP_400_BAD_REQUEST)
    if VerificationCodeModel.objects.filter(
                verUserProg=verification.verUserProg).exists() == False or verification.status == "A":
        #is_Active = False
        return False
    verification.verificationCode = verificationCode.data["userMail"]
    try:
        VerificationCodeModel.objects.create(
            verUserProg=verification.verUserProg,
            verificationCode=verificationCode.data["userMail"],
            verStartDate=verStartDate,
            verstatus="A",
            verStartDate=datetime.now(),
            verEndDate=verStartDate + timedelta(minutes=5))
    except:
        return Response({"errId": 1, "errMessage": "GEN001ERR"}, status=status.HTTP_400_BAD_REQUEST)
    return True
        
    


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
    if subService.data["mailVerificationCode"] != verification.verificationCode:
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
