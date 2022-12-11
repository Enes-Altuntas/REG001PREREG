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
    

    def __str__(self):
        return self.userName + ' ' + self.name + ' ' + self.surname


class CountryModel(models.Model):
    value = models.CharField(max_length=2)
    
    def __str__(self) -> str:
        return self.value