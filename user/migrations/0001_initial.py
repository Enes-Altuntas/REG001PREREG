# Generated by Django 4.1.4 on 2022-12-11 13:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CountryModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='UserModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userMail', models.CharField(max_length=50)),
                ('userCountryCode', models.CharField(max_length=2)),
                ('userPresenterId', models.IntegerField(blank=True, default=0)),
                ('userStatus', models.IntegerField(blank=True, null=True)),
                ('name', models.CharField(blank=True, max_length=30, null=True)),
                ('userName', models.CharField(blank=True, max_length=3, null=True)),
                ('surname', models.CharField(blank=True, max_length=30, null=True)),
                ('phonePrefix', models.CharField(blank=True, max_length=7, null=True)),
                ('userLanguage', models.CharField(blank=True, max_length=2, null=True)),
                ('phoneNumber', models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True)),
                ('acceptTermsCondition', models.CharField(blank=True, default='N', max_length=1)),
                ('acceptPrivacy', models.CharField(blank=True, default='N', max_length=1)),
                ('acceptStatistics', models.CharField(blank=True, default='N', max_length=1)),
                ('promoCode', models.CharField(blank=True, default='N', max_length=10)),
            ],
        ),
    ]