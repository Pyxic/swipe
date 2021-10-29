import rest_framework.mixins
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, status, generics, mixins
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from building.exceptions import AlreadyExist
from building.models import ResidentialComplex, Announcement, AnnouncementShot, Promotion, Complaint
from building.serializers import ResidentialComplexListSerializer, ResidentialComplexSerializer, \
    AnnouncementListSerializer, AnnouncementSerializer, GallerySerializer, PromotionSerializer, \
    PromotionRetrieveSerializer, ComplaintSerializer, ComplaintRejectSerializer
from building.services.filters import AnnouncementFilter


class ResidentComplexViewSet(viewsets.ModelViewSet):
    view_tags = ['residential complex']

    def get_queryset(self):
        return ResidentialComplex.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return ResidentialComplexListSerializer
        if self.action in ['retrieve', 'update', 'partial_update', 'destroy', 'create']:
            return ResidentialComplexSerializer


class AnnouncementViewSet(viewsets.ModelViewSet):
    filter_backends = (DjangoFilterBackend,)
    filterset_class = AnnouncementFilter
    view_tags = ['announcement']

    def get_queryset(self):
        return Announcement.objects.all().order_by('-created')

    def get_serializer_class(self):
        if self.action == 'list':
            return AnnouncementListSerializer
        if self.action in ['retrieve', 'update', 'partial_update', 'destroy', 'create']:
            return AnnouncementSerializer


class AnnouncementShotViewSet(viewsets.ModelViewSet):
    queryset = AnnouncementShot.objects.all()
    serializer_class = GallerySerializer
    view_tags = ['announcement']


class UserFavoritesViewSet(viewsets.ModelViewSet):
    queryset = Announcement.objects.filter(is_draft=True)
    view_tags = ['favorites']

    def get_serializer_class(self):
        if self.action == 'list':
            return AnnouncementListSerializer
        if self.action in ['destroy', 'create']:
            return AnnouncementSerializer

    def get_queryset(self):
        return self.queryset.filter(in_favorites=self.request.user)

    def create(self, request, *args, **kwargs):
        """check has already announcement in favorite and add to favorites if false"""
        announcement = get_object_or_404(Announcement, pk=request.data.get('announcement'))
        serializer = self.get_serializer(announcement)
        if request.user in announcement.in_favorites.all():
            raise AlreadyExist()
        announcement.in_favorites.add(request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        """remove from favorites"""
        announcement = get_object_or_404(Announcement, pk=request.data.get('announcement'))
        serializer = self.get_serializer(announcement)
        if request.user not in announcement.in_favorites.all():
            return Response(status=status.HTTP_404_NOT_FOUND)
        announcement.in_favorites.remove(request.user)
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)


class PromotionViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin,
                       mixins.UpdateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = Promotion.objects.all()
    lookup_field = 'announcement_id'
    view_tags = ['promotion']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return PromotionRetrieveSerializer
        return PromotionSerializer


class ComplaintViewSet(viewsets.ModelViewSet):
    queryset = Complaint.objects.filter(rejected=False).order_by('-created')
    view_tags = ['complaint']

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return ComplaintSerializer
        if self.action in ['update', 'partial_update']:
            return ComplaintRejectSerializer
