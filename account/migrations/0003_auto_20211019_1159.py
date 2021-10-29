# Generated by Django 3.2.8 on 2021-10-19 08:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Role')),
            ],
        ),
        migrations.RemoveField(
            model_name='developer',
            name='user',
        ),
        migrations.RemoveField(
            model_name='notary',
            name='user',
        ),
        migrations.AddField(
            model_name='user',
            name='client_agent',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='Client',
        ),
        migrations.DeleteModel(
            name='Developer',
        ),
        migrations.DeleteModel(
            name='Notary',
        ),
        migrations.AddField(
            model_name='user',
            name='role',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='account.role'),
        ),
    ]
