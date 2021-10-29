# Generated by Django 3.2.8 on 2021-10-26 06:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('building', '0008_auto_20211025_1727'),
    ]

    operations = [
        migrations.AlterField(
            model_name='announcement',
            name='calculation_options',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='announcement',
            name='heating_type',
            field=models.CharField(choices=[('центральное', 'центральное'), ('электрическое', 'электрическое'), ('водяное', 'водяное')], max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='announcement',
            name='latitude',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='announcement',
            name='longitude',
            field=models.FloatField(null=True),
        ),
    ]
