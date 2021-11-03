from datetime import date

from django.conf import settings
from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, permissions
from rest_framework.permissions import AllowAny

from account.models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics

from account.models import Role
from account.permissions import IsAdmin, IsOwner, IsAdminOrOwner, IsDeveloper
from account.serializers import RoleListSerializer, UserListSerializer, ClientUpdateSerializer, \
    NotaryDetailSerializer, ClientSerializer


@method_decorator(name='get', decorator=swagger_auto_schema(tags=['admin']))
class RoleListView(generics.ListAPIView):
    """Вывод списка ролей"""
    queryset = Role.objects.all()
    serializer_class = RoleListSerializer


class AdminViewSet(viewsets.ReadOnlyModelViewSet):
    view_tags = ['admin']
    serializer_class = UserListSerializer
    permission_classes = [IsAdmin]
    queryset = User.objects.filter(is_superuser=True)


class ClientViewSet(viewsets.ModelViewSet):
    view_tags = ['client']

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


class NotaryViewSet(viewsets.ViewSet):

    permission_classes = [IsAdmin]

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
    permission_classes = [IsAdmin]
    queryset = User.objects.filter(role__name='нотариус')
    serializer_class = NotaryDetailSerializer


@method_decorator(name='delete', decorator=swagger_auto_schema(tags=['notary']))
class NotaryDestroyView(generics.DestroyAPIView):
    """Удаление нотариуса"""
    permission_classes = [IsAdmin]
    queryset = User.objects.filter(role__name='нотариус')
    serializer_class = NotaryDetailSerializer


class DeveloperViewSet(viewsets.ModelViewSet):
    view_tags = ['developer']

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [IsAdmin]
        if self.action in ['update', 'partial_update', 'retrieve', 'destroy']:
            permission_classes = [IsAdminOrOwner]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        return User.objects.filter(role__name='застройщик')

    def get_serializer_class(self):
        if self.action == 'list':
            return UserListSerializer
        if self.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            return ClientSerializer


class ClientUpdateSubscriptionView(APIView):
    permission_classes = (permissions.IsAuthenticated, IsOwner)
    serializer_class = ClientUpdateSerializer
    view_tags = ['client']

    def patch(self, request, pk):
        user = get_object_or_404(User, id=pk)
        user.end_date = date.today().replace(month=1 if date.today().month // 12 == 1 else date.today().month + 1)
        user.subscribed = True
        user.save()
        return Response({'pk': user.pk, 'subscribed': user.subscribed,
                         'end_date': user.end_date.strftime('%Y-%m-%d')})


class ChangeBanStatus(APIView):
    permission_classes = (permissions.IsAuthenticated, IsAdmin)
    view_tags = ['admin']

    def patch(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        user.banned = not user.banned
        user.save()
        return Response({'pk': user.pk,
                         'ban': user.banned}, status=status.HTTP_200_OK)
