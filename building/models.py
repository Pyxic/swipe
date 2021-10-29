from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Advantage(models.Model):
    name = models.CharField('Название', max_length=100)


class ResidentialComplex(models.Model):
    name = models.CharField('Название', max_length=100)
    district = models.CharField('Район', max_length=50)
    microdistrict = models.CharField('Микрорайон', max_length=50)
    price_for_meter = models.PositiveIntegerField('Цена за 1 м2')
    min_area = models.FloatField('минимальная площадь')
    max_area = models.FloatField('максимальная площадь')
    frame_quantity = models.PositiveIntegerField('Кол-во корпусов')
    level_quantity = models.PositiveIntegerField()
    section_quantity = models.PositiveIntegerField()
    riser_quantity = models.PositiveIntegerField()

    class StatusComplex(models.TextChoices):
        flats = 'квартиры', _('квартиры')
        houses = 'коттеджи', _('коттеджи')
        new = 'новострой', _('новострой')

    class HouseType(models.TextChoices):
        apartment_house = 'многоквартирный', _('многоквартирный')
        private_house = 'частный', _('частный')

    class HouseClass(models.TextChoices):
        elite = 'элитный', _('элитный')
        new = 'новострой', _('новострой')
        old = 'хрущевка', _('хрущевка')

    class HouseTerritory(models.TextChoices):
        closed = 'закрытая', _('закрытая')
        guarded = 'охраняемая', _('охраняемая')
        closed_and_guarded = 'закрытая охраняемая', _('закрытая охраняемая')

    class HouseHeating(models.TextChoices):
        central = 'центральное', _('центральное')
        electric = 'электрическое', _('электрическое')
        water = 'водяное', _('водяное')

    class HouseSewerage(models.TextChoices):
        central = 'центральная', _('центральная')
        inner = 'внутренняя', _('внутренняя')
        outer = 'внешняя', _('внешняя')

    class HouseWaterSupply(models.TextChoices):
        central = 'центральное', _('центральное')
        gravity = 'самотечное', _('самотечное')
        combined = 'комбинированное', _('комбинированное')

    class HouseTechnology(models.TextChoices):
        monolithic = 'монолитный с каркассом', _('монолитный с каркассом')
        ceramic = 'керамические блоки', _('керамические блоки')

    status = models.CharField(choices=StatusComplex.choices, max_length=20, null=True)
    advantages = models.ManyToManyField(Advantage, null=True, blank=True)
    house_type = models.CharField(choices=HouseType.choices, max_length=30, null=True)
    house_class = models.CharField(choices=HouseClass.choices, max_length=30, null=True)
    house_territory = models.CharField(choices=HouseTerritory.choices, max_length=30, null=True)
    distance_to_sea = models.PositiveIntegerField(null=True)
    ceiling_height = models.PositiveIntegerField(default=3)
    is_gas = models.BooleanField(default=False)
    heating_type = models.CharField(choices=HouseHeating.choices, max_length=30, null=True)
    sewerage_type = models.CharField(choices=HouseSewerage.choices, max_length=30, null=True)
    water_supply_type = models.CharField(choices=HouseWaterSupply.choices, max_length=30, null=True)
    technology_of_building = models.CharField(choices=HouseTechnology.choices, max_length=40, null=True)
    longitude = models.FloatField(null=True)
    latitude = models.FloatField(null=True)
    registration = models.CharField("Оформление", max_length=30, null=True)
    calculation_options = models.CharField("Варианты расчета", max_length=30, null=True)
    appointment = models.CharField("Назначение", max_length=30, null=True)
    contract_amount = models.CharField("Неполная", max_length=30, null=True)
    address = models.CharField("Адрес", max_length=100, null=True)


class Document(models.Model):
    document = models.FileField(upload_to='house_documents')
    house = models.ForeignKey(ResidentialComplex, on_delete=models.CASCADE, related_name='documents')


class News(models.Model):
    title = models.CharField("Заголовок", max_length=100)
    description = models.TextField("Описание")
    complex = models.ForeignKey(ResidentialComplex, on_delete=models.CASCADE, related_name='news')


class Announcement(models.Model):
    address = models.CharField("Адрес", max_length=100)
    complex = models.ForeignKey(ResidentialComplex, on_delete=models.SET_NULL, null=True, related_name='flats')
    photo = models.ImageField(upload_to='announcements', null=True, blank=True)

    class FoundationDocument(models.TextChoices):
        own = 'собственность', _('собственность')
        gift = 'дар', _('дар')

    class AnnouncementAppointment(models.TextChoices):
        apartments = 'апартаменты', _('апартаменты')
        flat = 'квартира', _('квартира')
        private = 'частный дом', _('частный дом')

    class AnnouncementLayout(models.TextChoices):
        studio = 'студия', _('студия')
        isolate = 'изолированные коматы', _('изолированные комнаты')
        adjoining = 'смежные комнаты', _('смежные комнаты')

    class LivingCondition(models.TextChoices):
        new = 'новая', _('новая')
        need_repair = 'требует ремонта', _('требует ремонта')
        emergency = 'аварийное', _('аварийное')

    class CommunicationMethod(models.TextChoices):
        call = 'звонок', _('звонок')
        message = 'сообщение', _('сообщение')
        call_and_message = 'звонок и сообщение', _('звонок и сообщение')

    foundation_document = models.CharField(choices=FoundationDocument.choices, max_length=100)
    appointment = models.CharField(choices=AnnouncementAppointment.choices, max_length=100, null=True)
    room_quantity = models.PositiveIntegerField()
    layout = models.CharField(choices=AnnouncementLayout.choices, max_length=100)
    living_condition = models.CharField(choices=LivingCondition.choices, max_length=100)
    area = models.FloatField()
    kitchen_area = models.FloatField()
    has_balcony = models.BooleanField()
    heating_type = models.CharField(choices=ResidentialComplex.HouseHeating.choices, max_length=100, null=True)
    sewerage_type = models.CharField(choices=ResidentialComplex.HouseSewerage.choices, max_length=30, null=True)
    calculation_options = models.CharField(max_length=100, null=True)
    agent_commission = models.PositiveSmallIntegerField()
    communication_method = models.CharField(choices=CommunicationMethod.choices, max_length=100)
    description = models.TextField()
    price = models.PositiveIntegerField()
    longitude = models.FloatField(null=True)
    latitude = models.FloatField(null=True)
    is_draft = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    in_favorites = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='favorites')
    reject = models.BooleanField(default=False)
    reject_message = models.CharField(max_length=100, null=True)


class AnnouncementShot(models.Model):
    announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE, related_name='shots')
    image = models.ImageField(upload_to='gallery/%Y/%m/%d')

    def delete(self, *args, **kwargs):
        self.image.delete(save=False)
        super().delete(*args, **kwargs)


class Promotion(models.Model):
    PRICES = {
        'phrase': 199.0,
        'color': 199.0,
        'is_big': 399.0,
        'to_high': 399.0,
        'is_turbo': 499.0,
    }
    announcement = models.OneToOneField(Announcement, on_delete=models.CASCADE, related_name='promotion')
    phrase = models.CharField(max_length=255, null=True)
    color = models.CharField(max_length=7, null=True)
    is_big = models.BooleanField(default=False)
    to_high = models.BooleanField(default=False)
    is_turbo = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    finished = models.DateField()
    price = models.FloatField()

    def calculate_price(self):
        price = 0.0
        if self.phrase is not None:
            price += self.PRICES.get('phrase')
        if self.color is not None:
            price += self.PRICES.get('color')
        if self.is_big:
            price += self.PRICES.get('is_big')
        if self.to_high:
            price += self.PRICES.get('to_high')
        if self.is_turbo:
            price += self.PRICES.get('is_turbo')
        return price


class Complaint(models.Model):
    announcement = models.ForeignKey(Announcement, related_name='complaints', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='complaints', on_delete=models.CASCADE)
    description = models.TextField()
    rejected = models.BooleanField(default=False)
