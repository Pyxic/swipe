# Generated by Django 3.2.8 on 2021-10-20 15:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('building', '0002_auto_20211020_1639'),
    ]

    operations = [
        migrations.AlterField(
            model_name='residentialcomplex',
            name='status',
            field=models.CharField(choices=[('квартиры', 'квартиры'), ('коттеджи', 'коттеджи'), ('новострой', 'новострой')], max_length=20, null=True),
        ),
    ]
