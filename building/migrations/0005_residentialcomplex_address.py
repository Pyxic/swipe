# Generated by Django 3.2.8 on 2021-10-25 07:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('building', '0004_auto_20211025_1023'),
    ]

    operations = [
        migrations.AddField(
            model_name='residentialcomplex',
            name='address',
            field=models.CharField(max_length=100, null=True, verbose_name='Адрес'),
        ),
    ]
