# Generated by Django 4.1.4 on 2022-12-12 18:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_usermodel_userprog'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usermodel',
            name='userProg',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]