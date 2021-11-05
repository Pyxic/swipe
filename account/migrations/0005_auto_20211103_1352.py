# Generated by Django 3.2.8 on 2021-11-03 11:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_user_notification'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='banned',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='end_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='subscribed',
            field=models.BooleanField(default=False),
        ),
    ]