from .models import User
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
        fields = ('id', 'first_name', 'last_name', 'email', 'role')


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
            "password": {"write_only": True}
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
