# Generated by Django 4.1.4 on 2023-01-15 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0031_remove_usermodel_surname'),
    ]

    operations = [
        migrations.CreateModel(
            name='QRCodeModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('qr_code', models.ImageField(blank=True, null=True, upload_to='qr_codes')),
            ],
        ),
    ]
