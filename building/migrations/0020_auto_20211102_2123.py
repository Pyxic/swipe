# Generated by Django 3.2.8 on 2021-11-02 19:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('building', '0019_rename_levele_announcement_level'),
    ]

    operations = [
        migrations.AlterField(
            model_name='announcement',
            name='has_balcony',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='announcement',
            name='kitchen_area',
            field=models.FloatField(null=True),
        ),
    ]