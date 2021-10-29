from django.urls import path

from building import views

urlpatterns = [
        path('residential_complex', views.ResidentComplexViewSet.as_view({'get': 'list'})),
        path('residential_complex/<int:pk>', views.ResidentComplexViewSet.as_view({'get': 'retrieve'})),
        path('residential_complex_create', views.ResidentComplexViewSet.as_view({'post': 'create'})),
        path('residential_complex_update/<int:pk>', views.ResidentComplexViewSet.as_view({'put': 'update',
                                                                                          'patch': 'partial_update'})),
        path('residential_complex_delete/<int:pk>', views.ResidentComplexViewSet.as_view({'delete': 'destroy'})),
        path('announcement', views.AnnouncementViewSet.as_view({'get': 'list'})),
        path('announcement/<int:pk>', views.AnnouncementViewSet.as_view({'get': 'retrieve'})),
        path('announcement_create', views.AnnouncementViewSet.as_view({'post': 'create'})),
        path('announcement_update/<int:pk>', views.AnnouncementViewSet.as_view({'put': 'update',
                                                                                'patch': 'partial_update'})),
        path('announcement_delete/<int:pk>', views.AnnouncementViewSet.as_view({'delete': 'destroy'})),
        path('announcement_shot', views.AnnouncementShotViewSet.as_view({'get': 'list'})),
        path('announcement_shot/<int:pk>', views.AnnouncementShotViewSet.as_view({'get': 'retrieve'})),
        path('announcement_shot_create', views.AnnouncementShotViewSet.as_view({'post': 'create'})),
        path('announcement_shot_delee/<int:pk>', views.AnnouncementShotViewSet.as_view({'delete': 'destroy'})),
        path('favorites', views.UserFavoritesViewSet.as_view({'get': 'list'})),
        path('add_to_favorites', views.UserFavoritesViewSet.as_view({'post': 'create'})),
        path('remove_from_favorites', views.UserFavoritesViewSet.as_view({'delete': 'destroy'})),
        path('promotion/<int:announcement_id>', views.PromotionViewSet.as_view({'get': 'retrieve'})),
        path('promotion_update/<int:announcement_id>', views.PromotionViewSet.as_view({'put': 'update',
                                                                                       'patch': 'partial_update'})),
        path('promotion_create', views.PromotionViewSet.as_view({'post': 'create'})),
        path('complaint', views.ComplaintViewSet.as_view({'get': 'list'})),
        path('complaint/<int:pk>', views.ComplaintViewSet.as_view({'get': 'retrieve'})),
        path('complaint_create', views.ComplaintViewSet.as_view({'post': 'create'})),
        path('complaint_update/<int:pk>', views.ComplaintViewSet.as_view({'put': 'update'})),
    ]
