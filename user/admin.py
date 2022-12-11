from django.contrib import admin
from .models import UserModel, CountryModel

admin.site.register(UserModel)
admin.site.register(CountryModel)