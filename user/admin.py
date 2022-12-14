from django.contrib import admin
from .models import UserModel, CountryModel, UserApp, VerificationCodeModel

admin.site.register(UserModel)
admin.site.register(CountryModel)
admin.site.register(UserApp)
admin.site.register(VerificationCodeModel)
