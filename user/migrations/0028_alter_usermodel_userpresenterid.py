# Generated by Django 4.1.4 on 2023-01-13 16:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0027_alter_usermodel_userpresenterid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usermodel',
            name='userPresenterID',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
