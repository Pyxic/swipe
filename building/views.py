import mimetypes

import rest_framework.mixins
from django.db.models import Count, Q, Case, When
from django.http import FileResponse, HttpResponse
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.utils.decorators import method_decorator
from django.utils.encoding import escape_uri_path
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, status, generics, mixins, permissions
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from account.permissions import IsDeveloper, IsOwner, IsClient, IsAdminOrOwner, IsAdmin, IsOwnerOrReadOnly
from building.exceptions import AlreadyExist
from building.models import ResidentialComplex, Announcement, AnnouncementShot, Promotion, Complaint, RequestToChest, \
    News, Document
from building.serializers import ResidentialComplexListSerializer, ResidentialComplexSerializer, \
    AnnouncementListSerializer, AnnouncementSerializer, GallerySerializer, PromotionSerializer, \
    PromotionRetrieveSerializer, ComplaintSerializer, ComplaintRejectSerializer, AnnouncementModerationSerializer, \
    RequestToChestSerializer, NewsSerializer, DocumentSerializer
from building.services.filters import AnnouncementFilter


class ResidentComplexViewSet(viewsets.ModelViewSet):
    view_tags = ['residential complex']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [IsAuthenticated]
        if self.action in ['create']:
            permission_classes = [IsDeveloper]
        if self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsAdminOrOwner]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        return ResidentialComplex.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return ResidentialComplexListSerializer
        if self.action in ['retrieve', 'update', 'partial_update', 'destroy', 'create']:
            return ResidentialComplexSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class AnnouncementViewSet(viewsets.ModelViewSet):
    filter_backends = (DjangoFilterBackend,)
    filterset_class = AnnouncementFilter
    view_tags = ['announcement']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [AllowAny]
        if self.action in ['create']:
            permission_classes = [IsClient]
        if self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsAdminOrOwner]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        return Announcement.objects.filter(is_draft=True).\
            order_by('promotion', '-promotion__to_high', '-created')

    def get_serializer_class(self):
        if self.action == 'list':
            return AnnouncementListSerializer
        if self.action in ['retrieve', 'update', 'partial_update', 'destroy', 'create']:
            return AnnouncementSerializer

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)


class AnnouncementModerationAdminView(mixins.RetrieveModelMixin,
                                      mixins.UpdateModelMixin,
                                      mixins.ListModelMixin,
                                      viewsets.GenericViewSet):
    """
    Admin can get list of posts with complains or not approve
    """
    permission_classes = [IsAdmin]
    queryset = Announcement.objects.filter(is_draft=False, reject=False).order_by('-id')
    # Filter only posts with complaints
    serializer_class = AnnouncementSerializer
    view_tags = ['admin']

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return self.serializer_class
        if self.action in ('update', 'partial_update'):
            return AnnouncementModerationSerializer
        return self.serializer_class

    @action(detail=True, methods=['put', 'patch'])
    def approve_announcement(self, request, pk=None):
        announcement = self.get_object()
        announcement.is_draft = True
        announcement.reject = False
        announcement.reject_message = None
        announcement.save()
        return Response({'status': 'announcement approved'})

    @action(detail=True, methods=['patch'])
    def reject_announcement(self, request, pk=None):
        announcement = self.get_object()
        serializer = AnnouncementModerationSerializer(data=request.data, instance=announcement)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'announcement rejected'})
        else:
            return Response(serializer.errors)


class AnnouncementShotViewSet(viewsets.ModelViewSet):
    queryset = AnnouncementShot.objects.all()
    serializer_class = GallerySerializer
    view_tags = ['announcement']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [AllowAny]
        if self.action in ['create']:
            permission_classes = [IsClient]
        if self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsAdminOrOwner]
        return [permission() for permission in permission_classes]


class UserFavoritesViewSet(viewsets.ModelViewSet):
    queryset = Announcement.objects.filter(is_draft=True)
    view_tags = ['favorites']
    permission_classes = [IsAuthenticated]

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
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return PromotionRetrieveSerializer
        return PromotionSerializer


class ComplaintViewSet(viewsets.ModelViewSet):
    queryset = Complaint.objects.filter(rejected=False).order_by('-created')
    view_tags = ['complaint']

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdmin]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve', 'create']:
            return ComplaintSerializer
        if self.action in ['update', 'partial_update']:
            return ComplaintRejectSerializer


class RequestToChestCreateView(generics.CreateAPIView):
    """Добавление клиентом квартиры в шахматку"""
    serializer_class = RequestToChestSerializer
    permission_classes = [IsOwner]
    view_tags = ['client']


class RequestToChestViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin,
                            viewsets.GenericViewSet):
    serializer_class = RequestToChestSerializer
    permission_classes = [IsDeveloper]
    view_tags = ['developer']

    def get_queryset(self):
        return RequestToChest.objects.filter(residential_complex__user=self.request.user)

    @action(detail=True, methods=['put', 'delete'])
    def approve_request(self, request, pk=None):
        request_to_chest = self.get_object()
        announcement = request_to_chest.announcement
        announcement.residential_complex = request_to_chest.residential_complex
        announcement.save()
        request_to_chest.delete()
        return Response({"status": 'request to chest approved'})


class NewsViewSet(viewsets.ModelViewSet):
    serializer_class = NewsSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    queryset = News.objects.all().order_by('-id')
    view_tags = ['residential complex']

    def list(self, request, *args, **kwargs):
        """ Filter news by residential_complex """
        queryset = self.queryset.filter(residential_complex_id=request.query_params.get('residential_complex'))
        serializer = self.get_serializer(queryset, many=True)
        return Response(data=serializer.data)


class DocumentViewSet(viewsets.ModelViewSet):
    serializer_class = DocumentSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    queryset = Document.objects.all().order_by('-id')
    view_tags = ['residential complex']

    def list(self, request, *args, **kwargs):
        """ Filter documents by residential_complex """
        queryset = self.queryset.filter(residential_complex_id=request.query_params.get('residential_complex'))
        serializer = self.get_serializer(queryset, many=True)
        return Response(data=serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        with open(instance.document.path, 'rb') as file:
            file_name = instance.document.name.split('/')[-1].encode('utf-8')

            response = HttpResponse(file, content_type=mimetypes.guess_type(instance.document.name)[0])
            response['Content-Disposition'] = f'attachment; filename={escape_uri_path(file_name)}'
            return response
