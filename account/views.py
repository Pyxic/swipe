from django.conf import settings
from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from account.models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics

from account.models import Role
from account.permissions import IsAdmin, IsOwner, IsAdminOrOwner
from account.serializers import RoleListSerializer, UserListSerializer, ClientUpdateSerializer, \
    NotaryDetailSerializer, ClientSerializer


@method_decorator(name='get', decorator=swagger_auto_schema(tags=['user']))
class RoleListView(generics.ListAPIView):
    """Вывод списка ролей"""
    queryset = Role.objects.all()
    serializer_class = RoleListSerializer


@method_decorator(name='update', decorator=swagger_auto_schema(tags=['client']))
@method_decorator(name='partial_update', decorator=swagger_auto_schema(tags=['client']))
@method_decorator(name='list', decorator=swagger_auto_schema(tags=['client']))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(tags=['client']))
@method_decorator(name='destroy', decorator=swagger_auto_schema(tags=['client']))
class ClientViewSet(viewsets.ModelViewSet):

    def get_queryset(self):
        return User.objects.filter(role__name='клиент')

    def get_serializer_class(self):
        if self.action == 'list':
            return UserListSerializer
        if self.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            return ClientSerializer

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [AllowAny]
        if self.action in ['update', 'partial_update', 'retrieve']:
            permission_classes = [IsAdminOrOwner]
        return [permission() for permission in permission_classes]

# class ClientListView(generics.ListAPIView):
#     """Вывод списка клиентов"""
#     queryset = User.objects.filter(role__name='клиент')
#     serializer_class = UserListSerializer
#
#
# class ClientDetailView(generics.RetrieveAPIView):
#     """Вывод полной информации о клиенте"""
#     queryset = User.objects.filter(role__name='клиент')
#     serializer_class = ClientDetailSerializer


class NotaryViewSet(viewsets.ViewSet):

    @swagger_auto_schema(tags=['notary'])
    def list(self, request):
        """Вывод списка нотариусов"""
        queryset = User.objects.filter(role__name='нотариус')
        serializer = UserListSerializer(queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(tags=['notary'])
    def retrieve(self, request, pk=None):
        """Вывод полной информации о нотариусе"""
        queryset = User.objects.filter(role__name='нотариус')
        notary = get_object_or_404(queryset, pk=pk)
        serializer = NotaryDetailSerializer(notary)
        return Response(serializer.data)


@method_decorator(name='put', decorator=swagger_auto_schema(tags=['notary']))
@method_decorator(name='patch', decorator=swagger_auto_schema(tags=['notary']))
class NotaryUpdateView(generics.UpdateAPIView):
    """Редактирование нотариуса"""
    queryset = User.objects.filter(role__name='нотариус')
    serializer_class = NotaryDetailSerializer


@method_decorator(name='delete', decorator=swagger_auto_schema(tags=['notary']))
class NotaryDestroyView(generics.DestroyAPIView):
    """Удаление нотариуса"""
    queryset = User.objects.filter(role__name='нотариус')
    serializer_class = NotaryDetailSerializer


@method_decorator(name='update', decorator=swagger_auto_schema(tags=['user']))
@method_decorator(name='partial_update', decorator=swagger_auto_schema(tags=['user']))
@method_decorator(name='list', decorator=swagger_auto_schema(tags=['user']))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(tags=['user']))
@method_decorator(name='destroy', decorator=swagger_auto_schema(tags=['user']))
class DeveloperViewSet(viewsets.ModelViewSet):

    def get_queryset(self):
        return User.objects.filter(role__name='застройщик')

    def get_serializer_class(self):
        if self.action == 'list':
            return UserListSerializer
        if self.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            return ClientSerializer
