from django.db import models

class UserModel(models.Model):
    userMail = models.CharField(max_length=50)
    userCountryCode = models.CharField(max_length=2)
    userLanguage = models.CharField(max_length=2)
    userPresenterId = models.IntegerField(default=0,blank=True)
    userStatus = models.IntegerField(null=True,blank=True)
    name = models.CharField(max_length=30,blank=True,null=True)
    userName = models.CharField(max_length=3,blank=True,null=True)
    surname = models.CharField(max_length=30,blank=True,null=True)
    phonePrefix = models.CharField(max_length=7,blank=True,null=True)
    userLanguage = models.CharField(max_length=2,blank=True,null=True)
    phoneNumber = models.DecimalField(max_digits=20, decimal_places=2,null=True,blank=True)
    acceptTermsCondition = models.CharField(max_length=1,blank=True,default='N')
    acceptPrivacy = models.CharField(max_length=1,blank=True,default='N')
    acceptStatistics = models.CharField(max_length=1,blank=True,default='N')
    promoCode = models.CharField(max_length=10,blank=True,default='N')
    userProg = models.IntegerField(default=0,blank=True,null=True)
    userID = models.IntegerField(default=0,blank=True,null=True)
    
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
        return  str(self.appID)


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
