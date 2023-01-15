from django.urls import path
from . import views


urlpatterns = [
    path('reg001prereg', views.mainService),
    path('reg004verify', views.REG004PHONEVERIFY),
]
