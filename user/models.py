from django.db import models

class UserModel(models.Model):
    userMail = models.CharField(max_length=50)
    userCountryCode = models.CharField(max_length=2)
    userLanguage = models.CharField(max_length=2)
    userPresenterId = models.IntegerField()
    userStatus = models.IntegerField()
    name = models.CharField(max_length=30)
    userName = models.CharField(max_length=3)
    surname = models.CharField(max_length=30)
    phonePrefix = models.CharField(max_length=7)
    userLanguage = models.CharField(max_length=2)
    phoneNumber = models.DecimalField(max_digits=20, decimal_places=2)
    acceptTermsCondition = models.CharField(max_length=1)
    acceptPrivacy = models.CharField(max_length=1)
    acceptStatistics = models.CharField(max_length=1)
    promoCode = models.CharField(max_length=10)

    def __str__(self):
        return self.userName + ' ' + self.name + ' ' + self.surname
