import datetime
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .serializers import *
from user.models import *
from user.serializers import CountryCodeSerializer, UserSerializer, UserAppSerializer
from datetime import datetime , timedelta

# TODO:UPPERSTRING FOR ALL THE STRING INPUTS

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

    # CHANGE AFTER THAT CAUSE WE DONT HAVE THAT YET BUT ITS GOING TO BE A DROPDOWN
    if CountryModel.objects.filter(value=serviceOneSerializer.data["userCountryCode"]).exists() == True:
        return Response({"errId": 5, "errMessage": "Country code is already exist"}, status=status.HTTP_400_BAD_REQUEST)
    if UserModel.objects.filter(userPresenterID=serviceOneSerializer.data["userPresenterID"]).exists() == True:
        if int(serviceOneSerializer.data["userPresenterID"]) == UserModel.objects.get(userPresenterID=serviceOneSerializer.data["userPresenterID"]).userProg and UserModel.objects.get(userPresenterID=serviceOneSerializer.data["userPresenterID"]).userStatus > 4:
            return Response({"errId": 6, "errMessage": "Presenter ID already exists"}, status=status.HTTP_400_BAD_REQUEST)
    try:
        UserModel.objects.create(
            userMail=serviceOneSerializer.data["userMail"],
            userCountryCode=serviceOneSerializer.data["userCountryCode"],
            userLanguage=serviceOneSerializer.data["userLanguage"],
            userPresenterID=serviceOneSerializer.data["userPresenterID"],
            userStatus=1)
    except:
        return Response({"errId": 8, "errMessage": "DB Error"}, status=status.HTTP_400_BAD_REQUEST)

    # -------------------------------------------------------------------------------------------------------------

    # CHECK USER_USERTYPE
    if serviceOneSerializer.data["userType"] == "CU":
        try:
            CustomerModel.objects.create(cus_prog=1,
                                         cus_mail=serviceOneSerializer.data["userMail"])
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
            userProg=serviceTwoSerializer.data["userProg"]).userProg != serviceTwoSerializer.data["userProg"]:
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
            cus_prog=serviceThreeSerializer.data["userProg"])
        try:
            customer.cus_name = serviceThreeSerializer.data["name"].upper()
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
            userProg=serviceFiveSerializer.data["userProg"])
    except:
        return Response({"errId": 9, "errMessage": "User not found"}, status=status.HTTP_400_BAD_REQUEST)
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
    if serviceSixSerializer.is_valid() == False:
        return Response({"errId": 1, "errMessage": serviceSixSerializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    dbModel = UserModel.objects.get(
        userMail=serviceSixSerializer.data["userMail"])
    if REG012CHKPROMO(serviceSixSerializer.data) is False:
        return Response({"errId": 26, "errMessage": "GEN001ERR"}, status=status.HTTP_400_BAD_REQUEST)
    if dbModel.userMail != serviceSixSerializer.data["userMail"]:
        return Response({"errId": 9, "errMessage": serviceSixSerializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    if REG011IDCREATION(serviceSixSerializer.data) == False:
        return Response({"errId": 16, "errMessage": "GEN001ERR"}, status=status.HTTP_400_BAD_REQUEST)
    try:
        dbModel.promoCode = serviceSixSerializer.data["promoCode"]
        dbModel.userID = str(serviceSixSerializer.data["promoCode"])
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
            verUserProg=verification.verUserProg).exists() == False or verification.verstatus == "C":
        #is_Active = False
        return False
    try:
        VerificationCodeModel.objects.create(
            verUserProg=verification.verUserProg,
            verificationCode="AAA",
            verStartDate=verification.verStartDate,
            verstatus="A",
            verEndDate=datetime.now() + timedelta(minutes=5),
            verlastLoginerr=verification.verlastLoginerr,
            vercterr=1,
            verlasttentative=datetime.now())
    except:
        return Response({"errId": 1, "errMessage": "GEN001ERR"}, status=status.HTTP_400_BAD_REQUEST)
    return True
        
#vercode = random.randrange(10000, 99999)


def REG002PSWMNG(userData):
    user = UserModel.objects.get(userProg=userData["userProg"])
    password = PasswordModel.objects.get(passwordUserProg=userData["userProg"])
    passwordCheck = ServiceFiveSerializer(data=userData)
    if passwordCheck.is_valid():
        if "I" == passwordCheck.data["userFunctionType"]:
            if passwordCheck.data["userProg"] != user["userProg"]:
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
            if passwordCheck.data["userProg"] != user.userProg and password.passwordStartDate != password.passwordStartDate:
                return Response({"errId": 20, "errMessage": "GEN001ERR"}, status=status.HTTP_400_BAD_REQUEST)
            if password.passwordCterr == 5 and password.passwordStatus == "L":
                try:
                    password.passwordLastLogin = datetime.now()
                    password.passwordStatus = "L"
                    password.save()
                    return Response({"errId": 22, "errMessage": "GEN001ERR"}, status=status.HTTP_400_BAD_REQUEST)
                except:
                    return Response({"errId": 10, "errMessage": "Database error"}, status=status.HTTP_400_BAD_REQUEST)
            if datetime.now().minute > password.passwordEndDate.minute and password.passwordStatus == "E":
                try:
                    password.passwordStatus = "E"
                    password.passwordLastLogin = datetime.now()
                    password.save()
                    return Response({"errId": 21, "errMessage": "GEN001ERR"}, status=status.HTTP_400_BAD_REQUEST)
                except:
                    return Response({"errId": 10, "errMessage": "Database error"}, status=status.HTTP_400_BAD_REQUEST)
            if passwordCheck.data["password"] == password.passwordPassword:
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
    dbModel = UserModel.objects.get(userProg=userData["userProg"])
    dbModel.userID = dbModel.userCountryCode + str(userData["userProg"])

    return dbModel.userID


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
    if subService.data["verificationCode"] != verification.verificationCode:
        return Response({"errId": 23, "errMessage": "GEN001ERR"}, status=status.HTTP_400_BAD_REQUEST)
    if verification.vercterr != 5 and verification.verstatus == "L":
        try:
            verification.verstatus = "L"
            verification.verlastLoginerr = datetime.now()
            verification.save()
            return Response({"errId": 24, "errMessage": "GEN001ERR"}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"errId": 10, "errMessage": "Database error"}, status=status.HTTP_400_BAD_REQUEST)
    if datetime.now().minute < verification.verEndDate.minute:
        try:
            verification.verstatus = "E"
            verification.verlastLoginerr = datetime.now()
            verification.save()
            # return Response({"errId": 25, "errMessage": "GEN001ERR"}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"errId": 10, "errMessage": "Database error"}, status=status.HTTP_400_BAD_REQUEST)
    verification.verstatus = "A"
    if verification.verstatus == "E":
        return Response({"errId": 25, "errMessage": "GEN001ERR"}, status=status.HTTP_400_BAD_REQUEST)
    if verification.verstatus == "L":
        return Response({"errId": 23, "errMessage": "GEN001ERR"}, status=status.HTTP_400_BAD_REQUEST)
    if verification.verstatus == "A":
        try:
            verification.verlasttentative = datetime.now()
            verification.save()
        except:
            return Response({"errId": 10, "errMessage": "Database error"}, status=status.HTTP_400_BAD_REQUEST)


def REG004REGCUS(request):
    regCustomer = RegCustomerSerializer(data=request.data)
    if regCustomer.is_valid() == False:
        return Response({"errId": 1, "errMessage": regCustomer.errors}, status=status.HTTP_400_BAD_REQUEST)
    if UserModel.objects.filter(userProg=regCustomer.data["userProg"]).exists() == False:
        return Response({"errId": 2, "errMessage": "Invalid user"}, status=status.HTTP_400_BAD_REQUEST)
    if UserModel.objects.filter(userProg=regCustomer.data["userProg"]).userType != "CU":
        return Response({"errId": 3, "errMessage": "Invalid user type"}, status=status.HTTP_400_BAD_REQUEST)
    if CustomerModel.objects.filter(customerUserProg=regCustomer.data["userProg"]).exists() == False:
        return Response({"errId": 4, "errMessage": "Invalid customer prog"}, status=status.HTTP_400_BAD_REQUEST)
    user = UserModel.objects.get(userProg=regCustomer.data["userProg"])
    customer = CustomerModel.objects.get(
        customerUserProg=regCustomer.data["userProg"])
    return Response(user, customer, status=status.HTTP_200_OK)


def REG004REGCUSSUR(request):
    regCustomerSurnameSerializer = RegCustomerSurnameSerializer(
        data=request.data)
    if regCustomerSurnameSerializer.is_valid() == False:
        return Response({"errId": 1, "errMessage": regCustomerSurnameSerializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    if CustomerModel.objects.filter(cus_prog=regCustomerSurnameSerializer.data["userProg"]).exists() == False:
        return Response({"errId": 2, "errMessage": "Invalid customer prog"}, status=status.HTTP_400_BAD_REQUEST)
    customer = CustomerModel.objects.get(
        cus_prog=regCustomerSurnameSerializer.data["userProg"])
    try:
        customer.cus_surname = regCustomerSurnameSerializer.data["cus_surname"]
        customer.save()
    except:
        return Response({"errId": 3, "errMessage": "Database error"}, status=status.HTTP_400_BAD_REQUEST)


def REG004REGCUSNAME(request):
    regCustomerNameSerializer = RegCustomerNameSerializer(data=request.data)
    if regCustomerNameSerializer.is_valid() == False:
        return Response({"errId": 1, "errMessage": regCustomerNameSerializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    if CustomerModel.objects.filter(cus_prog=regCustomerNameSerializer.data["userProg"]).exists() == False:
        return Response({"errId": 2, "errMessage": "Invalid customer prog"}, status=status.HTTP_400_BAD_REQUEST)
    customer = CustomerModel.objects.get(
        cus_prog=regCustomerNameSerializer.data["userProg"])
    try:
        customer.cus_name = regCustomerNameSerializer.data["cus_name"]
        customer.save()
    except:
        return Response({"errId": 3, "errMessage": "Database error"}, status=status.HTTP_400_BAD_REQUEST)


def REG004REGCUSBDATE(request):
    regCustomerBdateSerializer = RegCustomerBdateSerializer(
        data=request.data)
    if regCustomerBdateSerializer.is_valid() == False:
        return Response({"errId": 1, "errMessage": regCustomerBdateSerializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    if CustomerModel.objects.filter(cus_prog=regCustomerBdateSerializer.data["userProg"]).exists() == False:
        return Response({"errId": 2, "errMessage": "Invalid customer prog"}, status=status.HTTP_400_BAD_REQUEST)
    customer = CustomerModel.objects.get(
        cus_prog=regCustomerBdateSerializer.data["userProg"])
    try:
        customer.cus_birthdate = regCustomerBdateSerializer.data["bdate"]
        customer.save()
    except:
        return Response({"errId": 3, "errMessage": "Database error"}, status=status.HTTP_400_BAD_REQUEST)




@api_view(['POST'])
def REG004PHONEVERIFY(request):
    if request.data["phone_callType"] == 1:
        phoneSerializer = PhoneSerializer(data=request.data)
        if phoneSerializer.is_valid() == False:
            return Response({"errId": 2, "errMessage": phoneSerializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        if UserModel.objects.filter(userProg=phoneSerializer.data["phone_userProg"]).exists() == False:
            return Response({"errId": 3, "errMessage": "Invalid_progr"}, status=status.HTTP_400_BAD_REQUEST)
        userProg = UserModel.objects.get(
            userProg=phoneSerializer.data["phone_userProg"]).userProg
        try:
            ChangePhone.objects.create(
                phone_userProg=userProg,
                phone_number=phoneSerializer.data["phone_phone"],
                phone_status=1,
                phone_endverification=datetime.now() + timedelta(minutes=5))
        except:
            return Response({"errId": 10, "errMessage": "Database error"}, status=status.HTTP_400_BAD_REQUEST)
        if REG007SENDVERCODE(phoneSerializer.data) == True:
            return Response({"errId": 0, "errMessage": "Success"}, status=status.HTTP_200_OK)
        else:
            return Response({"errId": 1, "errMessage": "GEN001ERR"}, status=status.HTTP_400_BAD_REQUEST)
    if request.data["phone_callType"] == 2:
        phoneSerializerVerify = PhoneSerializerVerify(data=request.data)
        if phoneSerializerVerify.is_valid() == False:
            return Response({"errId": 2, "errMessage": phoneSerializerVerify.errors}, status=status.HTTP_400_BAD_REQUEST)
        if UserModel.objects.filter(userProg=phoneSerializerVerify.data["phone_userProg"]).exists() == False:
            return Response({"errId": 3, "errMessage": "Invalid_progr"}, status=status.HTTP_400_BAD_REQUEST)
        if REG008CHECKVERCODE(phoneSerializerVerify.data) == False:
            return Response({"errId": 4, "errMessage": "GEN001ERR"}, status=status.HTTP_400_BAD_REQUEST)
        changePhone = ChangePhone.objects.get(
            userProg=phoneSerializerVerify.data["phone_userProg"])
        user = UserModel.objects.get(userProg=changePhone.phone_userProg)
        try:
            changePhone.phone_status = 2
            changePhone.phone_number = user.phoneNumber
            changePhone.phone_endvalidity = datetime.now()
            changePhone.phone_endverification = "0000-00-00 00:00:00"
        except:
            return Response({"errId": 10, "errMessage": "Database error"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user.phoneNumber = phoneSerializerVerify.data["phone_userPhone"]
            user.save()
        except:
            return Response({"errId": 10, "errMessage": "Database error"}, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['POST'])
# def commcrea(request):
#     input_language = request.data["input_language"],
#     input_caller = request.data["input_caller"],
#     input_ownerid = request.data["input_ownerid"],
#     input_ownercountry = request.data["input_ownercountry"],
#     input_presenterid = request.data["input_presenterid"]
#     print('commcrea-->', input_language, input_caller, input_ownerid, input_ownercountry,
#           input_presenterid)
#     error = None
#     service = 'cmty001isrt'
#     ownercountry = ''
#     presentercountry = ''

#     #rc, connection = dbconnection()

#     # if rc != 0:
#     #    error = connection
#     #    return rc, error

#     rc, error, ownercountry, presentercountry = checkdata(input_language,
#                                                           input_caller, input_ownerid, input_ownercountry, input_presenterid)

#     if rc == 0:
#         rc, error = process(input_language, input_ownerid, ownercountry,
#                             input_presenterid, presentercountry)

#     return rc, error


# def checkdata(input_language, input_caller, input_ownerid,
#               input_ownercountry, input_presenterid):

#     service = 'cmty001isrt'
#     ownercountry = ''
#     presentercountry = ''
#     rc = 0
#     error = None

#     if input_ownerid == '' or input_ownerid == None:
#         errid = 5
#         language = input_language
#         descr1 = input_ownerid
#         descr2 = ''

#         rc = 99
#         return rc, error, ownercountry, presentercountry
#     if input_language == '':
#         errid = 2
#         language = input_language
#         descr1 = input_language
#         descr2 = ''

#         rc = 99
#         return rc, error, ownercountry, presentercountry
#     else:
#         try:
#             cursor = connection.cursor()
#             querylanguage = "select lang_name from db999_services.language where lang_id = '{input_language}'""".format(
#                 input_language=input_language)
#             cursor.execute(querylanguage)
#             record = cursor.fetchone()
#             if record == None:
#                 errid = 2
#                 language = input_language
#                 descr1 = input_language
#                 descr2 = ''
#                 rc = 99
#                 return rc, error, ownercountry, presentercountry
#         except mysql.connector.Error as err:
#             errid = 999
#             language = input_language
#             descr1 = 'querylanguage'
#             descr2 = err
#             rc = 99
#             return rc, error, ownercountry, presentercountry
#     if input_caller == None:
#         errid = 9
#         language = input_language
#         descr1 = str(input_caller)
#         descr2 = ''
#         rc = 99
#         return rc, error
#     elif input_caller == 'front':
#         # read user for community owner
#         try:
#             cursor = connection.cursor()
#             queryuser = "select user_countrycode from db001_registro.user where user_progr = '{input_ownerid}'""".format(
#                 input_ownerid=input_ownerid)
#             cursor.execute(queryuser)
#             record = cursor.fetchone()
#             if record == None:
#                 errid = 5
#                 language = input_language
#                 descr1 = input_ownerid
#                 descr2 = ''
#                 rc = 99
#                 return rc, error
#             else:
#                 ownercountry = record[0]
#         except mysql as err:
#             errid = 999
#             language = input_language
#             descr1 = 'queryuser'
#             descr2 = err
#             rc = 99
#             return rc, error, ownercountry, presentercountry
#     elif input_caller == 'back':
#         ownercountry = input_ownercountry
#     else:
#         errid = 9
#         language = input_language
#         descr1 = str(input_caller)
#         descr2 = ''
#         rc = 99
#         return rc, error, ownercountry, presentercountry

#     # read user for presenterid
#     if input_presenterid == None:
#         presentercountry = ownercountry
#     else:
#         if input_presenterid == input_ownerid:
#             errid = 8
#             language = input_language
#             descr1 = str(input_ownerid)
#             descr2 = str(input_presenterid)
#             rc = 99
#             return rc, error, ownercountry, presentercountry
#         else:
#             try:
#                 cursor = connection.cursor()
#                 querypresenter = "select user_countrycode, user_status from db001_registro.user where user_progr = '{input_presenterid}'""".format(
#                     input_presenterid=input_presenterid)
#                 cursor.execute(querypresenter)
#                 record = cursor.fetchone()
#                 if record == None:
#                     errid = 6
#                     language = input_language
#                     descr1 = str(input_presenterid)
#                     descr2 = ''
#                     rc = 99
#                     return rc, error, ownercountry, presentercountry
#                 else:
#                     print('presenter status-->', record[1])
#                     if record[1] > 4:
#                         presentercountry = record[0]
#                     else:
#                         errid = 7
#                         language = input_language
#                         descr1 = str(input_presenterid)
#                         descr2 = ''
#                         rc = 99
#                         return rc, error, ownercountry, presentercountry
#             except mysql.connector.Error as err:
#                 errid = 999
#                 language = input_language
#                 descr1 = 'querypresenter'
#                 descr2 = err
#                 rc = 99
#                 return rc, error, ownercountry, presentercountry

#     return rc, error, ownercountry, presentercountry


# def process(connection, input_language, input_ownerid, ownercountry,
#             input_presenterid, presentercountry):
#     print('process-->', input_language, input_ownerid, ownercountry,
#           input_presenterid, presentercountry)
#     service = 'cmty001isrt'
#     rc = 0
#     error = None
#     if ownercountry == presentercountry:
#         rc, error = procsamecountries(connection, input_language, input_ownerid, ownercountry,
#                                       input_presenterid, presentercountry)
#     else:
#         rc, error = procdiffcountries(connection, input_language, input_ownerid,
#                                       input_presenterid, ownercountry, presentercountry)

#         if rc == 0:
#             rc, error = procsamecountries(connection, input_language, input_ownerid, ownercountry,
#                                           input_presenterid, presentercountry)

#     return rc, error


# def procsamecountries(connection, input_language, input_ownerid, ownercountry,
#                       input_presenterid, presentercountry):
#     print('samecountries', input_ownerid, ownercountry,
#           input_presenterid, presentercountry)
#     service = 'cmty001isrt'
#     rc = 0
#     error = None
#     # insert record community owner
#     level = 0
#     try:
#         cursor = connection.cursor()
#         isrtcommown = """insert into db002_community.community (cmty_ownerid, cmty_country,
#                          cmty_memberid, cmty_cmtylevel)
#             values
#             ('{input_ownerid}','{ownercountry}','{input_ownerid}','{level}')""".format(input_ownerid=input_ownerid, ownercountry=ownercountry, level=level)
#         cursor.execute(isrtcommown)
#         cursor.close()
#     except mysql.connector.Error as err:
#         errid = 999
#         language = input_language
#         descr1 = 'isrtcommown'
#         descr2 = err
#         rc = 99
#         return rc, error

#     # insert record histrewpoint
#     month = datetime.datetime.now().month
#     year = datetime.datetime.now().year
#     currenttime = datetime.datetime.now()
#     period = (''.join(str(year)+'-'+str(month)))

#     try:
#         cursor = connection.cursor()
#         isrthrewpoints = """insert into db002_community.histrewpoints
#         (hrew_userid, hrew_period, hrew_country, hrew_cmtycount, hrew_insertdate, hrew_lastupdate)
#              values
#              ('{input_ownerid}','{period}', '{ownercountry}', 1, '{currenttime}','{currenttime}' )""".format(input_ownerid=input_ownerid, period=period, ownercountry=ownercountry, currenttime=currenttime)

#         cursor.execute(isrthrewpoints)
#         cursor.close()
#     except mysql.connector.Error as err:
#         errid = 999
#         language = input_language
#         descr1 = 'isrthrewpoints'
#         descr2 = err
#         rc = 99
#         return rc, error

#     # insert rows in db Community to update owner and presenter communities:
#     try:
#         cursor = connection.cursor()
#         querycomm = """select cmty_ownerid, cmty_country, cmty_memberid, cmty_cmtylevel from db002_community.community
#              where cmty_memberid = '{input_presenterid}' and cmty_country = '{ownercountry}' order by cmty_cmtylevel """.format(input_presenterid=input_presenterid, ownercountry=ownercountry)
#         cursor.execute(querycomm)
#         records = cursor.fetchall()
#         for row in records:
#             owner = row[0]
#             memberid = input_ownerid
#             cmtylevel = row[3] + 1
#             rc, error = inscmnty(connection, input_language,
#                                  owner, ownercountry, memberid, cmtylevel)
#         cursor.close()
#     except mysql.connector.Error as err:
#         errid = 999
#         language = input_language
#         descr1 = 'querycomm'
#         descr2 = err
#         rc = 99
#         return rc, error
#     rc, error = updatectr(connection, input_language,
#                           input_ownerid, ownercountry)
#     return rc, error


# def updatectr(connection, input_language, input_ownerid, ownercountry):
#     print('update ctr-->', input_ownerid, ownercountry)
#     service = 'cmty001isrt'
#     rc = 0
#     error = None
#     currenttime = datetime.datetime.now()
#     # update friends and community ctr for community owner:
#     try:
#         cursor = connection.cursor()
#         queryupdtctrown = """update db002_community.histrewpoints,
#                 (select * FROM db002_community.community
#                     where cmty_cmtylevel = 1 and cmty_memberid = '{input_ownerid}'
#                         and cmty_country = '{ownercountry}')
#                     AS community
#            SET hrew_cmtycount = hrew_cmtycount + 1,
# 	           hrew_friendscount = hrew_friendscount + 1,
# 	           hrew_lastupdate = '{currenttime}'
#            WHERE hrew_userid = community.cmty_ownerid and
#                hrew_country = '{ownercountry}'""".format(input_ownerid=input_ownerid, ownercountry=ownercountry, currenttime=currenttime)
#         cursor.execute(queryupdtctrown)
#         print(cursor.rowcount, "Record updated successfully into table hrew",
#               input_ownerid, ownercountry)
#         cursor.close
#     except mysql.connector.Error as err:
#         errid = 999
#         language = input_language
#         descr1 = 'queryupdtctrown'
#         descr2 = err
#         rc = 99
#         return rc, error

#     # update community ctr for community upper levels:
#     try:
#         cursor = connection.cursor()
#         queryupdtctrcom = """update db002_community.histrewpoints,
#                 (select * FROM db002_community.community
#                     where cmty_cmtylevel > 1 and cmty_memberid = '{input_ownerid}'
#                     and cmty_country = '{ownercountry}')
#                     AS community
#             SET hrew_cmtycount = hrew_cmtycount + 1,
# 	            hrew_lastupdate = '{currenttime}'
#             WHERE hrew_userid = community.cmty_ownerid and
#                 hrew_country = '{ownercountry}'""".format(input_ownerid=input_ownerid, ownercountry=ownercountry, currenttime=currenttime)
#         cursor.execute(queryupdtctrcom)
#         print(cursor.rowcount, "Record updated successfully into table hrew2",
#               input_ownerid, ownercountry)
#         cursor.close
#     except mysql.connector.Error as err:
#         errid = 999
#         language = input_language
#         descr1 = 'queryupdtctrcom'
#         descr2 = err
#         rc = 99
#         return rc, error

#     return rc, error


# def inscmnty(connection, input_language, owner, ownercountry, memberid, cmtylevel):
#     service = 'cmty001isrt'
#     rc = 0
#     error = None
#     try:
#         cursor = connection.cursor()
#         isrtcomm = """insert into db002_community.community (cmty_ownerid, cmty_country,
#                                         cmty_memberid, cmty_cmtylevel, cmty_status)
#             values
#             ('{owner}','{ownercountry}','{memberid}','{cmtylevel}','P')""".format(owner=owner, ownercountry=ownercountry, memberid=memberid, cmtylevel=cmtylevel)

#         cursor.execute(isrtcomm)
#         cursor.close()
#         return rc, error
#     except mysql.connector.Error as err:
#         errid = 999
#         language = input_language
#         descr1 = 'isrtcomm'
#         descr2 = err
#         rc = 99
#         return rc, error


# def procdiffcountries(connection, input_language, input_ownerid, input_presenterid,
#                       ownercountry, presentercountry):
#     print('diffcountries', input_ownerid, input_presenterid,
#           ownercountry, presentercountry)
#     service = 'cmty001isrt'
#     rc = 0
#     error = None
#     # check if presenter id has already its community in the country
#     try:
#         print('check presenter', input_presenterid, ownercountry)
#         cursor = connection.cursor()
#         querycommpres = """select cmty_ownerid from db002_community.community
#             where cmty_ownerid = '{input_presenterid}' and cmty_country = '{ownercountry}'
#                 and cmty_cmtylevel = 0""".format(input_presenterid=input_presenterid, ownercountry=ownercountry)

#         cursor.execute(querycommpres)
#         record = cursor.fetchone()
#         print('record', record)
#         if record == None:
#             rc, error = isrtcommpres(connection, input_language, input_ownerid,
#                                      input_presenterid, ownercountry, presentercountry)
#         cursor.close()
#         return rc, error
#     except mysql.connector.Error as err:
#         errid = 999
#         language = input_language
#         descr1 = 'querycommpres'
#         descr2 = err
#         rc = 99
#         return rc, error


# def isrtcommpres(connection, input_language, input_ownerid, input_presenterid,
#                  ownercountry, presentercountry):
#     print('isrt presenter community', input_language, input_ownerid, input_presenterid,
#           ownercountry, presentercountry)
#     service = 'cmty001isrt'
#     rc = 0
#     error = None
#     # read presenter community and insert records for new country

#     try:
#         print('read presenter community', input_presenterid, presentercountry)

#         cursor = connection.cursor()
#         queryprescmty = """select * from db002_community.community
#             where cmty_memberid in
#                         (select cmty_ownerid from db002_community.community
# 			                    where cmty_memberid = '{input_presenterid}'
#                                 and cmty_country = '{presentercountry}')
#                 and cmty_country = '{presentercountry}'
#                 order by cmty_ownerid desc, cmty_cmtylevel""".format(input_presenterid=input_presenterid, presentercountry=presentercountry)

#         cursor.execute(queryprescmty)
#         record = cursor.fetchall()
#         own = None
#         ctrfriends = 0
#         ctrcmty = 0
#         for row in record:
#             if own == None:
#                 own = row[0]
#             #   print ('own fuori ciclo', own)
#             #print ('row upper level', row)
#             rc, error = isrtnewcountry(connection, input_language, row[0], ownercountry,
#                                        row[2], row[3])
#             if rc != 0:
#                 return rc, error
#             level = row[3]
#             if row[0] == own:
#                 # if level == 1:
#                 #    ctrfriends = ctrfriends + 1
#                 #    ctrcmty = ctrcmty + 1
#                 #    print('friend di', own, '=', ctrfriends)
#                 #    print('cmty di', own, '=', ctrcmty)
#                 # else:
#                 #    ctrcmty = ctrcmty + 1
#                 print('cmty di', own, level)
#             else:
#                 rc, error = isrthrew(connection, input_language, own,
#                                      ownercountry, ctrfriends, ctrcmty, level)
#                 if rc == 0:
#                     own = row[0]
#                     ctrfriends = 0
#                     ctrcmty = 0
#                     level = row[3]
#                     # if level == 1:
#                     #   ctrfriends = ctrfriends + 1
#                     #   ctrcmty = ctrcmty + 1
#                     #   print('friend di', own, '=', ctrfriends)
#                     #    print('cmty di', own, '=', ctrcmty)
#                     # else:
#                     #    ctrcmty = ctrcmty + 1
#                     #    print('cmty di', own, '=', ctrcmty)
#                 else:
#                     return rc, error
#         rc, error = isrthrew(connection, input_language, own,
#                              ownercountry, ctrfriends, ctrcmty, level)
#         if rc != 0:
#             return rc, error
#         cursor.close()

#     except mysql.connector.Error as err:
#         errid = 999
#         language = input_language
#         descr1 = 'queryprescmty'
#         descr2 = err
#         rc = 99
#         return rc,

#     return rc, error


# def isrtnewcountry(connection, input_language, ownerid, country, memberid, level):
#     print('isrtnewcountry', ownerid, country, memberid, level)
#     service = 'cmty001isrt'
#     rc = 0
#     error = None
#     # check if presenter id has already its community in the country
#     try:
#         print('check row cmty already present', ownerid, country)
#         cursor = connection.cursor()
#         querycheckcmty = """select cmty_ownerid from db002_community.community
#             where cmty_ownerid = '{ownerid}' and cmty_country = '{country}'
#             and cmty_memberid = '{memberid}'""".format(ownerid=ownerid, country=country, memberid=memberid)

#         cursor.execute(querycheckcmty)
#         record = cursor.fetchone()
#         #print ('recordcmty', record)
#         # if not present insert row with owner country
#         if record == None:
#             try:
#                 print('isrt cmty row', ownerid, country, memberid, level)
#                 #cursor = connection.cursor()
#                 isrtcmtyrow = """insert into db002_community.community (cmty_ownerid, cmty_country,
#                             cmty_memberid, cmty_cmtylevel, cmty_status)
#                 values
#                 ('{ownerid}','{country}','{memberid}','{level}', 'A')""".format(ownerid=ownerid, country=country, memberid=memberid, level=level)
#                 cursor.execute(isrtcmtyrow)
#                 cursor.close()
#             except mysql.connector.Error as err:
#                 errid = 999
#                 language = input_language
#                 descr1 = 'isrtcmtyrow'
#                 descr2 = err
#                 rc = 99
#                 return rc, error

#     except mysql.connector.Error as err:
#         errid = 999
#         language = input_language
#         descr1 = 'querycommpres'
#         descr2 = err
#         rc = 99
#         return rc, error
#     print('insrt country 2 ok', ownerid)
#     return rc, error


# def isrthrew(connection, input_language, ownerid, country, ctrfriends, ctrcmty, level):
#     service = 'cmty001isrt'
#     rc = 0
#     error = None
#     month = datetime.datetime.now().month
#     year = datetime.datetime.now().year
#     currenttime = datetime.datetime.now()
#     period = (''.join(str(year)+'-'+str(month)))
#     # check if presenter id has already its community in the country
#     try:
#         print('check row hrew already present', ownerid, period, country)
#         cursor = connection.cursor()
#         querycheckhrew = """select hrew_userid from db002_community.histrewpoints
#             where hrew_userid = '{ownerid}' and hrew_country = '{country}'
#             and hrew_period = '{period}'""".format(ownerid=ownerid, country=country, period=period)

#         cursor.execute(querycheckhrew)
#         record = cursor.fetchone()
#         #print ('recordcmty', record)
#         # if not present insert row with owner country
#         if record == None:
#             # insert record histrewpoint
#             try:
#                 cursor = connection.cursor()
#                 isrthrew2 = """insert into db002_community.histrewpoints
#                 (hrew_userid, hrew_period, hrew_country, hrew_friendscount,
#                                             hrew_cmtycount, hrew_insertdate, hrew_lastupdate)
#                 values
#                 ('{ownerid}', '{period}', '{country}', '{ctrfriends}', '{ctrcmty}','{currenttime}',
#                     '{currenttime}')""".format(ownerid=ownerid, period=period, country=country, ctrfriends=ctrfriends, ctrcmty=ctrcmty, currenttime=currenttime)

#                 cursor.execute(isrthrew2)
#                 cursor.close()
#             except mysql.connector.Error as err:
#                 errid = 999
#                 language = input_language
#                 descr1 = 'isrthrew2'
#                 descr2 = err
#                 rc = 99
#                 return rc, error
#         # update ctr histrewpoint
#         rc, error = updatectrnnewcountry(connection, input_language, ownerid,
#                                          country, period, level)
#     except mysql.connector.Error as err:
#         errid = 999
#         language = input_language
#         descr1 = 'querycheckhrew'
#         descr2 = err
#         rc = 99
#         return rc, error
#     print('insrt hrew ok', ownerid)
#     return rc, error


# def updatectrnnewcountry(connection, input_language, ownerid, ownercountry, period, level):
#     print('update ctr new ->', ownerid, ownercountry, period, level)
#     service = 'cmty001isrt'
#     rc = 0
#     error = None
#     try:
#         cursor = connection.cursor()
#         querycountfriends = """select count(*) from db002_community.community
#                     WHERE cmty_ownerid = '{ownerid}' and
#                             cmty_country = '{ownercountry}'
#                             and cmty_cmtylevel = 1
#                     """.format(ownerid=ownerid, ownercountry=ownercountry)
#         cursor.execute(querycountfriends)
#         riga = cursor.fetchall()
#         for row in riga:
#             ctrfriends = int(row[0])
#         print('community di ', ownerid, ownercountry)
#         print('friends = ', ctrfriends)
#         cursor.close
#     except mysql.connector.Error as err:
#         errid = 999
#         language = input_language
#         descr1 = 'querycountfriends'
#         descr2 = err
#         rc = 99
#         return rc, error

#     try:
#         cursor = connection.cursor()
#         querycountcmty = """select count(*) from db002_community.community
#                     WHERE cmty_ownerid = '{ownerid}' and
#                             cmty_country = '{ownercountry}'
#                     """.format(ownerid=ownerid, ownercountry=ownercountry)
#         cursor.execute(querycountcmty)
#         riga = cursor.fetchall()
#         for row in riga:
#             ctrcmty = int(row[0])
#         print('community = ', ctrcmty)
#         cursor.close
#     except mysql.connector.Error as err:
#         errid = 999
#         language = input_language
#         descr1 = 'querycountcmty'
#         descr2 = err
#         rc = 99
#         return rc, error

#     currenttime = datetime.datetime.now()
#     try:
#         cursor = connection.cursor()
#         queryupdtctrown2 = """update db002_community.histrewpoints
#                 SET hrew_cmtycount = '{ctrcmty}',
# 	                hrew_friendscount = '{ctrfriends}',
# 	                hrew_lastupdate = '{currenttime}'
#                 WHERE hrew_userid = '{ownerid}' and
#                     hrew_country = '{ownercountry}' and
#                     hrew_period = '{period}'""".format(ctrcmty=ctrcmty, ctrfriends=ctrfriends, ownerid=ownerid, ownercountry=ownercountry, period=period, currenttime=currenttime)
#         cursor.execute(queryupdtctrown2)
#         print(cursor.rowcount, "Record updated successfully into table hrew2",
#               ownerid, ownercountry, period)
#         cursor.close
#     except mysql.connector.Error as err:
#         errid = 999
#         language = input_language
#         descr1 = 'queryupdtctrown2'
#         descr2 = err
#         rc = 99
#         return rc, error
#     return rc, error


# def updatectrnnewcountryold(connection, input_language, ownerid, ownercountry, period, level):
#     print('update ctr new old ->', ownerid, ownercountry, period, level)
#     service = 'cmty001isrt'
#     rc = 0
#     error = None
#     currenttime = datetime.datetime.now()
#     if level == 1:
#         # update friends and community ctr for community owner:
#         try:
#             cursor = connection.cursor()
#             queryupdtctrown2 = """update db002_community.histrewpoints,
#                 SET hrew_cmtycount = hrew_cmtycount + 1,
# 	                hrew_friendscount = hrew_friendscount + 1,
# 	                hrew_lastupdate = '{currenttime}'
#                 WHERE hrew_userid = '{ownerid}' and
#                     hrew_country = '{ownercountry}'
#                     hrew_period = '{period}'""".format(ownerid=ownerid, ownercountry=ownercountry, period=period, currenttime=currenttime)
#             cursor.execute(queryupdtctrown2)
#             print(cursor.rowcount, "Record updated successfully into table hrew2",
#                   ownerid, ownercountry, period)
#             cursor.close
#         except mysql.connector.Error as err:
#             errid = 999
#             language = input_language
#             descr1 = 'queryupdtctrown2'
#             descr2 = err
#             rc = 99
#             return rc, error
#     elif level > 1:
#         # update community ctr for other levels:
#         try:
#             cursor = connection.cursor()
#             queryupdtctrcom2 = """update db002_community.histrewpoints
#                 SET hrew_cmtycount = hrew_cmtycount + 1,
# 	                hrew_lastupdate = '{currenttime}'
#                 WHERE hrew_userid = '{ownerid}' and
#                     hrew_country = '{ownercountry}' and
#                     hrew_period = '{period}'""".format(ownerid=ownerid, ownercountry=ownercountry, period=period, currenttime=currenttime)
#             cursor.execute(queryupdtctrcom2)
#             print(cursor.rowcount, "Record updated successfully into table hrew2",
#                   ownerid, ownercountry)
#             cursor.close
#         except mysql.connector.Error as err:
#             errid = 999
#             language = input_language
#             descr1 = 'queryupdtctrcom2'
#             descr2 = err
#             rc = 99
#             return rc, error

#     return rc, error
