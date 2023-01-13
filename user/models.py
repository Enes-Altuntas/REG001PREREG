from django.db import models
import uuid

# ALL PROGS SHOULD BE PRIMARY KEY
# USER PRESENTERID SHOULD BE CHARFIELD WITH 16 CHARACTERS

class UserModel(models.Model):

    userMail = models.CharField(max_length=50)
    userCountryCode = models.CharField(max_length=2)
    userLanguage = models.CharField(max_length=2)
    userPresenterID = models.IntegerField(default=0, blank=True, null=True)
    userStatus = models.IntegerField(null=True, blank=True)
    phonePrefix = models.CharField(max_length=7, blank=True, null=True)
    userLanguage = models.CharField(max_length=2, blank=True, null=True)
    phoneNumber = models.DecimalField(
        max_digits=20, decimal_places=2, null=True, blank=True)
    acceptTermsCondition = models.CharField(
        max_length=1, blank=True, default='N')
    acceptPrivacy = models.CharField(max_length=1, blank=True, default='N')
    acceptStatistics = models.CharField(max_length=1, blank=True, default='N')
    promoCode = models.CharField(max_length=10, blank=True, default='N')
    userProg = models.IntegerField(
        primary_key=True, default=1, editable=False)
    userID = models.CharField(blank=True, null=True, max_length=50)
    functionType = models.CharField(max_length=1, blank=True, null=True)
    userType = models.CharField(max_length=2, blank=True, null=True)
    user_mail2 = models.CharField(max_length=50, blank=True, null=True)
    user_maildelegat = models.CharField(max_length=50, blank=True, null=True)
    user_phonenumber2 = models.DecimalField(
        max_digits=20, decimal_places=2, null=True, blank=True)

    class Meta:
        db_table = 'user'

    def __str__(self):
        return str(self.userName)


class LanguageModel(models.Model):
    value = models.CharField(max_length=2)

    class Meta:
        db_table = 'language'

    def __str__(self) -> str:
        return self.value


class CountryModel(models.Model):
    value = models.CharField(max_length=2)

    class Meta:
        db_table = 'country'

    def __str__(self) -> str:
        return self.value


class UserApp(models.Model):
    userProg = models.IntegerField()
    appID = models.IntegerField()
    userStatus = models.IntegerField()

    class Meta:
        db_table = 'user_app'

    def __str__(self) -> int:
        return str(self.appID)


class VerificationCodeModel(models.Model):
    verUserProg = models.IntegerField()
    verCodeType = models.CharField(max_length=1)
    verStartDate = models.DateTimeField()
    verEndDate = models.DateTimeField()
    verlastLoginerr = models.DateTimeField()
    verstatus = models.CharField(max_length=1)
    vercterr = models.IntegerField()
    verlasttentative = models.DateTimeField()
    verificationCode = models.CharField(max_length=6, default='000000')

    class Meta:
        db_table = 'verification_code'

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

    class Meta:
        db_table = 'password'

    def __str__(self) -> str:
        return self.password

# TODO: PRimary key as customer prog


class CustomerModel(models.Model):
    cus_prog = models.IntegerField(unique=True)
    cus_name = models.CharField(max_length=30, blank=True, null=True)
    cus_mail = models.CharField(max_length=50, blank=True, null=True)
    cus_surname = models.CharField(max_length=30, blank=True, null=True)
    cus_address = models.CharField(max_length=50, blank=True, null=True)
    cus_birthdate = models.DateField(blank=True, null=True)
    cus_docimgfrontid = models.CharField(max_length=10, blank=True, null=True)
    cus_docimgackid = models.CharField(max_length=10, blank=True, null=True)
    cus_residenceproofimg = models.CharField(
        max_length=10, blank=True, null=True)
    cus_vatcode = models.CharField(max_length=30, blank=True, null=True)
    cus_companyprogr = models.IntegerField(blank=True, null=True)
    cus_companyrole = models.BooleanField(blank=True, null=True)
    cus_companyauthlevel = models.BooleanField(blank=True, null=True)
    cus_nationalid = models.CharField(max_length=30, blank=True, null=True)
    cus_docendvalidity = models.DateField(blank=True, null=True)

    class Meta:
        db_table = 'customer'

    def __str__(self) -> str:
        return self.cus_name


class CompanyModel(models.Model):
    comp_prog = models.IntegerField(unique=True, auto_created=True)
    comp_mail = models.CharField(max_length=50, blank=True, null=True)
    comp_name = models.CharField(max_length=100, blank=True, null=True)
    comp_address = models.CharField(max_length=200, blank=True, null=True)
    comp_legalrepprogr = models.IntegerField(blank=True, null=True)
    comp_legalrepname = models.CharField(max_length=30, blank=True, null=True)
    comp_legalrepsurname = models.CharField(
        max_length=30, blank=True, null=True)
    comp_legalrpcountry = models.CharField(max_length=2, blank=True, null=True)
    comp_legalrepmail = models.CharField(max_length=50, blank=True, null=True)
    comp_legalrepdocimgfrontid = models.CharField(
        max_length=10, blank=True, null=True)
    comp_legalrepdocimgackid = models.CharField(
        max_length=10, blank=True, null=True)
    comp_vatcode = models.CharField(max_length=30, blank=True, null=True)
    comp_sectorid = models.CharField(max_length=3,  blank=True, null=True)
    comp_legalrepdocendvalidity = models.DateField(blank=True, null=True)

    class Meta:
        db_table = 'company'

    def __str__(self) -> str:
        return self.comp_name


class ExpertModel(models.Model):
    user_id = models.PositiveIntegerField(unique=True)
    exp_prog = models.IntegerField()
    expert_mail = models.EmailField(unique=True)
    business_name = models.CharField(max_length=30)
    document_type = models.CharField(max_length=2)
    document_id = models.CharField(max_length=15)
    document_image_front = models.ImageField()
    document_image_back = models.ImageField()
    vat_code = models.CharField(max_length=30)
    job_sector_id = models.CharField(max_length=3)

    class Meta:
        db_table = 'expert'

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

    class Meta:
        db_table = 'app'

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

    class Meta:
        db_table = 'plan_app'

    def __str__(self) -> str:
        return self.plan_name


class PlanDetails(models.Model):
    plan = models.CharField(max_length=10)
    row_progr = models.PositiveSmallIntegerField(unique=True)
    field_name = models.CharField(max_length=10)
    field_type = models.CharField(max_length=1)
    field_value = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        db_table = 'plan_details'

    def __str__(self) -> str:
        return self.plan + self.row_progr


class Profile(models.Model):
    profile = models.CharField(max_length=10, unique=True)
    app_code = models.CharField(max_length=3, unique=True)
    status = models.BooleanField()
    profile_name = models.CharField(max_length=10)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)

    class Meta:
        db_table = 'profile'

    def __str__(self) -> str:
        return self.profile_name


class PromoCode(models.Model):
    promo_promocode = models.CharField(max_length=10, unique=True)
    promo_appid = models.CharField(max_length=3, unique=True)
    promo_desc = models.CharField(max_length=100)
    promo_status = models.BooleanField()
    promo_startdate = models.DateField()
    promo_enddate = models.DateField()

    class Meta:
        db_table = 'promo_code'

    def __str__(self) -> str:
        return self.promo_promocode


class UserPayMet(models.Model):
    user_id = models.PositiveIntegerField(unique=True)
    payment_method = models.CharField(max_length=3)
    payment_method_progr = models.PositiveSmallIntegerField(unique=True)
    payment_method_id = models.CharField(max_length=30)
    payment_method_user_note = models.CharField(
        max_length=30, blank=True, null=True)

    class Meta:
        db_table = 'user_pay_met'

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

    class Meta:
        db_table = 'error_codes'


abs = [{
    'error_code': 1,
    'description': [{'Wrong call type'}, {"asd": "asd"}]
}]
