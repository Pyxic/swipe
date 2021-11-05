from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.mail import send_mail
from django.conf import settings

from .managers import UserManager
from django.utils.translation import ugettext_lazy as _
from django.db import models


class Role(models.Model):
    name = models.CharField('Role', max_length=50)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    is_active = models.BooleanField(_('active'), default=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    phone = models.CharField("phone", max_length=17)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, null=True)
    client_agent = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,
                                     related_name='agent')
    subscribed = models.BooleanField(default=False)
    end_date = models.DateField(blank=True, null=True)
    banned = models.BooleanField(default=False)

    class Notification(models.TextChoices):
        me = 'мне', _('мне')
        me_and_agent = 'мне и агенту', _('мне и агенту')
        agent = 'агенту', _('агенту')
        off = 'отключить', _('отключить')
    notification = models.CharField(choices=Notification.choices, max_length=50, default=Notification.me)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """
        Returns the short name for the user.
        """
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email], **kwargs)

    @property
    def user(self):
        return User.objects.get(id=self.id)


class UserFilter(models.Model):
    market_choices = (
        ('NOVOSTROY', _('Новострой')),
        ('SECONDARY', _('Вторичный рынок')),
        ('COTTAGES', _('Коттеджи')),
        ('ALL', _('Все')),
    )
    number_of_rooms_choices = (
        (1, _('1 комната')),
        (2, _('2 комнаты')),
        (3, _('3 комнаты')),
        (4, _('4 комнаты')),
        (5, _('Больше 4-х комнат'))
    )
    status_choices = (
        ('FLATS', _('Квартиры')),
        ('OFFICES', _('Офисы'))
    )
    payment_conditions_choices = (
        ('MORTGAGE', _('Ипотека')),
        ('CAPITAL', _('Материнский капитал')),
        ('PAYMENT', _('Прямая оплата'))
    )
    state_choices = (
        ('ROUGH', _('Черновая')),
        ('READY', _('В жилом состоянии')),
        ('RENOVATION', _('Требует ремонта'))
    )
    LIMIT = 3  # Max filters for unsubscribed users

    name = models.CharField(max_length=100, blank=True, null=True)
    user = models.ForeignKey(User, related_name='filters', on_delete=models.CASCADE)
    market = models.CharField(choices=market_choices, default='ALL', max_length=9, blank=True, null=True)
    type = models.CharField(max_length=10, blank=True, null=True)
    status = models.CharField(choices=status_choices, default='FLATS', max_length=7, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    #  city stores as regular string because we get all locations from all houses
    address = models.CharField(max_length=100, blank=True, null=True)
    number_of_rooms = models.IntegerField(choices=number_of_rooms_choices, default=1,
                                          blank=True, null=True)
    min_price = models.IntegerField(blank=True, null=True)
    max_price = models.IntegerField(blank=True, null=True)
    min_square = models.FloatField(blank=True, null=True)
    max_square = models.FloatField(blank=True, null=True)
    payment_cond = models.CharField(choices=payment_conditions_choices, max_length=10, blank=True, null=True)
    state = models.CharField(choices=state_choices, max_length=10, blank=True, null=True)
