from django.db import models

#MODELS

class UserModel(models.Model):

    userMail = models.CharField(max_length=50)
    userCountryCode = models.CharField(max_length=2)
    userLanguage = models.CharField(max_length=2)
    userPresenterId = models.IntegerField(default=0, blank=True)
    userStatus = models.IntegerField(null=True, blank=True)
    name = models.CharField(max_length=30, blank=True, null=True)
    userName = models.CharField(max_length=3, blank=True, null=True)
    surname = models.CharField(max_length=30, blank=True, null=True)
    phonePrefix = models.CharField(max_length=7, blank=True, null=True)
    userLanguage = models.CharField(max_length=2, blank=True, null=True)
    phoneNumber = models.DecimalField(
        max_digits=20, decimal_places=2, null=True, blank=True)
    acceptTermsCondition = models.CharField(
        max_length=1, blank=True, default='N')
    acceptPrivacy = models.CharField(max_length=1, blank=True, default='N')
    acceptStatistics = models.CharField(max_length=1, blank=True, default='N')
    promoCode = models.CharField(max_length=10, blank=True, default='N')
    userProg = models.IntegerField(default=0, blank=True, null=True)
    userID = models.IntegerField(default=0, blank=True, null=True)

    def __str__(self):
        return str(self.userName)


class CountryModel(models.Model):
    value = models.CharField(max_length=2)

    def __str__(self) -> str:
        return self.value


class UserApp(models.Model):
    userProg = models.IntegerField()
    appID = models.IntegerField()
    userStatus = models.IntegerField()

    def __str__(self) -> int:
        return str(self.appID)


class VerificationCodeModel(models.Model):
    verUserProg = models.IntegerField()
    verCodeType = models.CharField(max_length=1)
    verStartDate = models.DateTimeField()
    verEndDate = models.DateTimeField()
    lastLoginerr = models.DateTimeField()
    status = models.CharField(max_length=1)
    cterr = models.IntegerField()
    lasttentative = models.DateTimeField()
    verificationCode = models.CharField(max_length=6, default='000000')

    def __str__(self) -> str:
        return self.verificationCode


class PasswordModel(models.Model):
    passwordPassword = models.CharField(max_length=50)
    passwordUserProg = models.IntegerField()
    passworduserMail = models.CharField(max_length=50)
    passwordStatus = models.CharField(max_length=1)
    passwordLastLogin = models.DateTimeField()
    passwordEndDate = models.DateTimeField()
    passwordStartDate = models.DateTimeField()
    passwordCterr = models.IntegerField()

    def __str__(self) -> str:
        return self.password


class Customer(models.Model):
    cus_progr = models.IntegerField(unique=True)
    cus_name = models.CharField(max_length=30)
    cus_surname = models.CharField(max_length=30)
    cus_address1 = models.CharField(max_length=50)
    cus_address2 = models.CharField(max_length=50, blank=True, null=True)
    cus_city = models.CharField(max_length=30)
    cus_postcode = models.CharField(max_length=30)
    cus_birthdate = models.DateField(blank=True, null=True)
    cus_doctype = models.CharField(max_length=2)
    cus_docid = models.CharField(max_length=20)
    cus_docimgfrontid = models.CharField(max_length=10)
    cus_docimgackid = models.CharField(max_length=10)
    cus_residenceproofimg = models.CharField(max_length=10)
    cus_vatcode = models.CharField(max_length=30)
    cus_companyprogr = models.IntegerField(blank=True, null=True)
    cus_companyrole = models.BooleanField()
    cus_companyauthlevel = models.BooleanField()

    def __str__(self) -> str:
        return self.cus_name


class CompanyModel(models.Model):
    comp_progr = models.IntegerField(unique=True)
    comp_mail = models.EmailField(unique=True)
    comp_name = models.CharField(max_length=50)
    comp_address1 = models.CharField(max_length=50)
    comp_address2 = models.CharField(max_length=50, blank=True, null=True)
    comp_city = models.CharField(max_length=30)
    comp_postcode = models.CharField(max_length=30)
    comp_legalrepprogr = models.IntegerField(blank=True, null=True)
    comp_legalrepname = models.CharField(max_length=30)
    comp_legalrepsurname = models.CharField(max_length=30)
    comp_legalrpcountry = models.CharField(max_length=2)
    comp_legalrepmail = models.EmailField()
    comp_legalrepdoctype = models.CharField(max_length=2)
    comp_legalrepdocid = models.CharField(max_length=20)
    comp_legalrepdocimgfrontid = models.CharField(max_length=10)
    comp_legalrepdocimgackid = models.CharField(max_length=10)
    comp_vatcode = models.CharField(max_length=30)
    comp_sectorid = models.CharField(max_length=3)

    def __str__(self) -> str:
        return self.comp_name


class Expert(models.Model):
    user_id = models.PositiveIntegerField(unique=True)
    expert_mail = models.EmailField(unique=True)
    business_name = models.CharField(max_length=30)
    document_type = models.CharField(max_length=2)
    document_id = models.CharField(max_length=15)
    document_image_front = models.ImageField()
    document_image_back = models.ImageField()
    vat_code = models.CharField(max_length=30)
    job_sector_id = models.CharField(max_length=3)

    def __str__(self) -> str:
        return self.business_name


class App(models.Model):
    app_appid = models.CharField(max_length=3, unique=True)
    app_name = models.CharField(max_length=15)
    app_description = models.CharField(max_length=100)
    app_status = models.BooleanField()
    app_link = models.CharField(max_length=60)
    app_usertypeauth = models.CharField(max_length=1)
    app_startdate = models.DateField()
    app_enddate = models.DateField(blank=True, null=True)

    def __str__(self) -> str:
        return self.app_name


class PlanApp(models.Model):
    plan = models.CharField(max_length=10, unique=True)
    app_code = models.CharField(max_length=3, unique=True)
    status = models.BooleanField()
    plan_name = models.CharField(max_length=10)
    currency = models.CharField(max_length=3)
    cost = models.DecimalField(max_digits=5, decimal_places=2)
    duration = models.PositiveSmallIntegerField()
    duration_type = models.CharField(max_length=1)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)

    def __str__(self) -> str:
        return self.plan_name


class PlanDetails(models.Model):
    plan = models.CharField(max_length=10)
    row_progr = models.PositiveSmallIntegerField(unique=True)
    field_name = models.CharField(max_length=10)
    field_type = models.CharField(max_length=1)
    field_value = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self) -> str:
        return self.plan + self.row_progr


class Profile(models.Model):
    profile = models.CharField(max_length=10, unique=True)
    app_code = models.CharField(max_length=3, unique=True)
    status = models.BooleanField()
    profile_name = models.CharField(max_length=10)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)

    def __str__(self) -> str:
        return self.profile_name


class PromoCode(models.Model):
    promo_promocode = models.CharField(max_length=10, unique=True)
    promo_appid = models.CharField(max_length=3, unique=True)
    promo_desc = models.CharField(max_length=100)
    promo_status = models.BooleanField()
    promo_startdate = models.DateField()
    promo_enddate = models.DateField()

    def __str__(self) -> str:
        return self.promo_promocode


class UserPayMet(models.Model):
    user_id = models.PositiveIntegerField(unique=True)
    payment_method = models.CharField(max_length=3)
    payment_method_progr = models.PositiveSmallIntegerField(unique=True)
    payment_method_id = models.CharField(max_length=30)
    payment_method_user_note = models.CharField(
        max_length=30, blank=True, null=True)

    def __str__(self) -> str:
        return self.payment_method


class errorCodes:
    error_codes = [
        {'error_code': 1, 'description': 'Wrong call type'},
        {'error_code': 2, 'description': 'Missing mandatory data'},
        {'error_code': 3, 'description': 'User_mail already registered'},
        {'error_code': 4, 'description': [{"1": "Waiting for mail validation"}, {"2": "Waiting for phone validation"}, {
            "3": "Waiting for additional info from pe-registration"}, {"4": "Waiting for additional info from pe-registration"}, {"5": "Pre-registration phase completed"}]},
        {'error_code': 5, 'description': 'Invalid Country code'},
        {'error_code': 6, 'description': 'Presenter not valid'},
        {'error_code': 7, 'description': 'Unsuccessfull mail validation'},
        {'error_code': 8, 'description': 'Unsuccessfull insert table'},
        {'error_code': 9, 'description': 'User mail not valid'},
        {'error_code': 10, 'description': 'Unsuccessfull update table'},
        {'error_code': 12, 'description': 'Unsuccessfull phone validation'},
        {'error_code': 13, 'description': 'Invalid Application Code'},
        {'error_code': 14, 'description': 'Unsuccessfull password validation'},
        {'error_code': 16, 'description': 'Unsuccessfull ID creation'},
        {'error_code': 17, 'description': 'Password already registered'},
        {'error_code': 18, 'description': 'Password not numeric'},
        {'error_code': 19, 'description': 'Invalid old password'},
        {'error_code': 20, 'description': 'Invalid password'},
        {'error_code': 21, 'description': 'Expired password'},
        {'error_code': 22, 'description': 'Locked password'},
        {'error_code': 23, 'description': 'Invalid verification code'},
        {'error_code': 24, 'description': 'Locked verification code'},
        {'error_code': 25, 'description': 'Expired verification code'},
        {'error_code': 26, 'description': 'Invalid Promo'},
        {'error_code': 28, 'description': 'Failed Verification code'},
        {'error_code': 29, 'description': 'Missing error code'},
        {'error_code': 30, 'description': 'UserID not valid'},
        {'error_code': 31, 'description': ''},
    ]


abs = [{
    'error_code': 1,
    'description': [{'Wrong call type'}, {"asd": "asd"}]
}]
