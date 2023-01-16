# Generated by Django 4.1.4 on 2023-01-16 15:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0034_changephone'),
    ]

    operations = [
        migrations.RenameField(
            model_name='usermodel',
            old_name='acceptPrivacy',
            new_name='user_acceptPrivacy',
        ),
        migrations.RenameField(
            model_name='usermodel',
            old_name='acceptStatistics',
            new_name='user_acceptStatistics',
        ),
        migrations.RenameField(
            model_name='usermodel',
            old_name='acceptTermsCondition',
            new_name='user_acceptTermsCondition',
        ),
        migrations.RenameField(
            model_name='usermodel',
            old_name='functionType',
            new_name='user_functionType',
        ),
        migrations.RenameField(
            model_name='usermodel',
            old_name='phoneNumber',
            new_name='user_phoneNumber',
        ),
        migrations.RenameField(
            model_name='usermodel',
            old_name='phonePrefix',
            new_name='user_phonePrefix',
        ),
        migrations.RenameField(
            model_name='usermodel',
            old_name='promoCode',
            new_name='user_promoCode',
        ),
        migrations.RenameField(
            model_name='usermodel',
            old_name='userCountryCode',
            new_name='user_userCountryCode',
        ),
        migrations.RenameField(
            model_name='usermodel',
            old_name='userID',
            new_name='user_userID',
        ),
        migrations.RenameField(
            model_name='usermodel',
            old_name='userLanguage',
            new_name='user_userLanguage',
        ),
        migrations.RenameField(
            model_name='usermodel',
            old_name='userMail',
            new_name='user_userMail',
        ),
        migrations.RenameField(
            model_name='usermodel',
            old_name='userPresenterID',
            new_name='user_userPresenterID',
        ),
        migrations.RenameField(
            model_name='usermodel',
            old_name='userProg',
            new_name='user_userProg',
        ),
        migrations.RenameField(
            model_name='usermodel',
            old_name='userStatus',
            new_name='user_userStatus',
        ),
        migrations.RenameField(
            model_name='usermodel',
            old_name='userType',
            new_name='user_userType',
        ),
        migrations.RenameField(
            model_name='usermodel',
            old_name='user_mail2',
            new_name='user_user_mail2',
        ),
        migrations.RenameField(
            model_name='usermodel',
            old_name='user_maildelegat',
            new_name='user_user_maildelegat',
        ),
        migrations.RenameField(
            model_name='usermodel',
            old_name='user_phonenumber2',
            new_name='user_user_phonenumber2',
        ),
    ]