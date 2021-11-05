# Generated by Django 3.2.8 on 2021-11-05 08:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_auto_20211103_1352'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserFilter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('market', models.CharField(blank=True, choices=[('NOVOSTROY', 'Новострой'), ('SECONDARY', 'Вторичный рынок'), ('COTTAGES', 'Коттеджи'), ('ALL', 'Все')], default='ALL', max_length=9, null=True)),
                ('type', models.CharField(blank=True, max_length=10, null=True)),
                ('status', models.CharField(blank=True, choices=[('FLATS', 'Квартиры'), ('OFFICES', 'Офисы')], default='FLATS', max_length=7, null=True)),
                ('city', models.CharField(blank=True, max_length=100, null=True)),
                ('address', models.CharField(blank=True, max_length=100, null=True)),
                ('number_of_rooms', models.IntegerField(blank=True, choices=[(1, '1 комната'), (2, '2 комнаты'), (3, '3 комнаты'), (4, '4 комнаты'), (5, 'Больше 4-х комнат')], default=1, null=True)),
                ('min_price', models.IntegerField(blank=True, null=True)),
                ('max_price', models.IntegerField(blank=True, null=True)),
                ('min_square', models.FloatField(blank=True, null=True)),
                ('max_square', models.FloatField(blank=True, null=True)),
                ('payment_cond', models.CharField(blank=True, choices=[('MORTGAGE', 'Ипотека'), ('CAPITAL', 'Материнский капитал'), ('PAYMENT', 'Прямая оплата')], max_length=10, null=True)),
                ('state', models.CharField(blank=True, choices=[('ROUGH', 'Черновая'), ('READY', 'В жилом состоянии'), ('RENOVATION', 'Требует ремонта')], max_length=10, null=True)),
            ],
        ),
    ]
