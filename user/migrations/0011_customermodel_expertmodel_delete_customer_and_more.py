# Generated by Django 4.1.4 on 2023-01-02 10:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0010_usermodel_functiontype'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cus_prog', models.IntegerField(unique=True)),
                ('cus_name', models.CharField(max_length=30)),
                ('cus_mail', models.EmailField(max_length=254, unique=True)),
                ('cus_surname', models.CharField(max_length=30)),
                ('cus_address1', models.CharField(max_length=50)),
                ('cus_address2', models.CharField(blank=True, max_length=50, null=True)),
                ('cus_city', models.CharField(max_length=30)),
                ('cus_postcode', models.CharField(max_length=30)),
                ('cus_birthdate', models.DateField(blank=True, null=True)),
                ('cus_doctype', models.CharField(max_length=2)),
                ('cus_docid', models.CharField(max_length=20)),
                ('cus_docimgfrontid', models.CharField(max_length=10)),
                ('cus_docimgackid', models.CharField(max_length=10)),
                ('cus_residenceproofimg', models.CharField(max_length=10)),
                ('cus_vatcode', models.CharField(max_length=30)),
                ('cus_companyprogr', models.IntegerField(blank=True, null=True)),
                ('cus_companyrole', models.BooleanField()),
                ('cus_companyauthlevel', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='ExpertModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.PositiveIntegerField(unique=True)),
                ('exp_prog', models.IntegerField()),
                ('expert_mail', models.EmailField(max_length=254, unique=True)),
                ('business_name', models.CharField(max_length=30)),
                ('document_type', models.CharField(max_length=2)),
                ('document_id', models.CharField(max_length=15)),
                ('document_image_front', models.ImageField(upload_to='')),
                ('document_image_back', models.ImageField(upload_to='')),
                ('vat_code', models.CharField(max_length=30)),
                ('job_sector_id', models.CharField(max_length=3)),
            ],
        ),
        migrations.DeleteModel(
            name='Customer',
        ),
        migrations.DeleteModel(
            name='Expert',
        ),
        migrations.RenameField(
            model_name='companymodel',
            old_name='comp_progr',
            new_name='comp_prog',
        ),
        migrations.AddField(
            model_name='usermodel',
            name='userType',
            field=models.CharField(blank=True, max_length=1, null=True),
        ),
    ]
