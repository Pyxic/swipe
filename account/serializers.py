import datetime

from . import choices
from .models import User, UserFilter
from rest_framework import serializers
from djoser.serializers import UserCreateSerializer as BaseUserRegistrationSerializer

from account.models import Role


class UserRegistrationSerializer(BaseUserRegistrationSerializer):
    class Meta(BaseUserRegistrationSerializer.Meta):
        fields = ('email', 'first_name', 'last_name', 'role', 'phone', 'password')


class UserListSerializer(serializers.ModelSerializer):
    """основная информация о пользователях"""

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'role', 'avatar', 'banned')


class RecursiveSerializer(serializers.Serializer):
    """Выввод рекурсии"""
    def to_representation(self, value):
        serializer = self.parent.client_agent.__class__(value, content=self.context)
        return serializer.data


class AgentSerializer(serializers.ModelSerializer):
    """Информация об агенте клиента"""

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email')


class ClientSerializer(UserListSerializer):
    """Полная информация о клиенте"""
    agent = RecursiveSerializer(read_only=True, many=True)

    class Meta:
        model = User
        fields = "__all__"
        extra_kwargs = {
            "password": {"write_only": True},
            "end_date": {"read_only": True},
            "subscribed": {"read_only": True},
            "ban": {"read_only": True}
        }

    def create(self, validated_data):
        email = validated_data("email")
        password = validated_data("password")
        first_name = validated_data("first_name")
        last_name = validated_data("last_name")
        user = User(email=email, first_name=first_name, last_name=last_name)
        user.set_password(password)
        user.save()
        return validated_data

    def update(self, instance, validated_data):
        for validated_field, value in validated_data.items():
            if validated_field == "password":
                password = validated_data.get("password")
                instance.set_password(password)
                continue
            setattr(instance, validated_field, value)
        instance.save()
        return instance


class ClientUpdateSerializer(serializers.ModelSerializer):
    """Полная информация о клиенте"""
    email = serializers.EmailField(required=False)
    phone = serializers.CharField(required=False, max_length=17)

    class Meta:
        model = User
        exclude = ('password',)


class NotaryDetailSerializer(serializers.ModelSerializer):
    """Полная информация о нотариусе"""
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email')


class UserCreateSerializer(serializers.ModelSerializer):
    """Создание пользователя"""

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'role', 'password')


class RoleListSerializer(serializers.ModelSerializer):
    """Список ролей пользователей"""

    class Meta:
        model = Role
        fields = "__all__"


class UserFilterSerializer(serializers.Serializer):
    living_type = serializers.ChoiceField(choices=choices.type_choices, required=False)
    payment_options = serializers.ChoiceField(choices=choices.payment_options_choices, required=False)
    price__gte = serializers.IntegerField(required=False)
    price__lte = serializers.IntegerField(required=False)
    flat__square__gte = serializers.IntegerField(required=False)
    flat__square__lte = serializers.IntegerField(required=False)
    flat__state = serializers.ChoiceField(choices=choices.state_choices, required=False)
    house__status = serializers.ChoiceField(choices=choices.status_choices, required=False)
    house__city = serializers.CharField(required=False)
    house__address = serializers.CharField(required=False)
    name = serializers.CharField(required=False)

    def create(self, validated_data):
        user_filter = UserFilter.objects.create(market=validated_data.get('living_type'),
                                                payment_cond=validated_data.get('payment_options'),
                                                min_price=validated_data.get('price__gte'),
                                                max_price=validated_data.get('price__lte'),
                                                min_square=validated_data.get('flat__square__gte'),
                                                max_square=validated_data.get('flat__square__lte'),
                                                status=validated_data.get('house__status'),
                                                city=validated_data.get('house__city'),
                                                address=validated_data.get('house__address'),
                                                number_of_rooms=validated_data.get('flat__number_of_rooms'),
                                                state=validated_data.get('flat__state'),
                                                user=validated_data.get('user'),
                                                name=validated_data.get('name',
                                                                        datetime.date.today().strftime('%Y-%m-%d')))
        return user_filter

    def update(self, instance, validated_data):
        instance.market = validated_data.get('living_type', instance.market)
        instance.payment_cond = validated_data.get('payment_options', instance.payment_cond)
        instance.min_price = validated_data.get('price__gte', instance.min_price)
        instance.max_price = validated_data.get('price__lte', instance.max_price)
        instance.min_square = validated_data.get('flat__square__gte', instance.min_square)
        instance.max_square = validated_data.get('flat__square__lte', instance.max_square)
        instance.status = validated_data.get('house__status', instance.status)
        instance.city = validated_data.get('house__city', instance.city)
        instance.address = validated_data.get('house__address', instance.address)
        instance.number_of_rooms = validated_data.get('flat__number_of_rooms', instance.number_of_rooms)
        instance.state = validated_data.get('flat__state', instance.state)
        instance.name = validated_data.get('name', instance.name)
        return instance

    def to_representation(self, instance):
        """
        We need to check if instance attribute empty or not. Because query params cant handle 'None' value
        Also, Django`s filter lookups can take 'None' or empty string as a valid filter value.
        So, we have to return dictionary only with valid values
        :param instance:
        :return: dict
        """
        data = {'saved_filter_pk': instance.pk}
        if instance.market:
            data['living_type'] = instance.market
        if instance.payment_cond:
            data['payment_options'] = instance.payment_cond
        if instance.min_price:
            data['price__gte'] = instance.min_price
        if instance.max_price:
            data['price__lte'] = instance.max_price
        if instance.min_square:
            data['flat__square__gte'] = instance.min_square
        if instance.max_square:
            data['flat__square__lte'] = instance.max_square
        if instance.status:
            data['house__status'] = instance.status
        if instance.city:
            data['house__city'] = instance.city
        if instance.address:
            data['house__address'] = instance.address
        if instance.number_of_rooms:
            data['flatt__number_of_rooms'] = instance.number_of_rooms
        if instance.state:
            data['flat__state'] = instance.state
        if instance.name:
            data['name'] = instance.name

        return data


class UserRoleSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('role',)
