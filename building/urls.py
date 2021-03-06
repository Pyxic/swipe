from django.urls import path

from building import views

urlpatterns = [
        path('residential_complex', views.ResidentComplexViewSet.as_view({'get': 'list'}), name='list-complex'),
        path('residential_complex/<int:pk>', views.ResidentComplexViewSet.as_view({'get': 'retrieve'}),
             name='detail-complex'),
        path('residential_complex_create', views.ResidentComplexViewSet.as_view({'post': 'create'}),
             name='create-complex'),
        path('residential_complex_update/<int:pk>', views.ResidentComplexViewSet.as_view({'put': 'update',
                                                                                          'patch': 'partial_update'})),
        path('residential_complex_delete/<int:pk>', views.ResidentComplexViewSet.as_view({'delete': 'destroy'})),
        path('announcement', views.AnnouncementViewSet.as_view({'get': 'list'}), name='list-announcement'),
        path('announcement/<int:pk>', views.AnnouncementViewSet.as_view({'get': 'retrieve'}),
             name='detail-announcement'),
        path('announcement_create', views.AnnouncementViewSet.as_view({'post': 'create'}), name='create-announcement'),
        path('announcement_update/<int:pk>', views.AnnouncementViewSet.as_view({'put': 'update',
                                                                                'patch': 'partial_update'})),
        path('announcement_delete/<int:pk>', views.AnnouncementViewSet.as_view({'delete': 'destroy'})),
        path('announcement_shot', views.AnnouncementShotViewSet.as_view({'get': 'list'})),
        path('announcement_shot/<int:pk>', views.AnnouncementShotViewSet.as_view({'get': 'retrieve'})),
        path('announcement_shot_create', views.AnnouncementShotViewSet.as_view({'post': 'create'})),
        path('announcement_shot_delete/<int:pk>', views.AnnouncementShotViewSet.as_view({'delete': 'destroy'})),
        path('user_announcement', views.UserAnnouncementViewSet.as_view({'get': 'list'})),
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
        path('announcement_moderation', views.AnnouncementModerationAdminView.as_view({'get': 'list'}),
             name='list-announcement-moderation'),
        path('announcement_moderation/<int:pk>', views.AnnouncementModerationAdminView.as_view({'get': 'retrieve'}),
             name='detail-announcement-moderation'),
        path('announcement_moderation_approve/<int:pk>',
             views.AnnouncementModerationAdminView.as_view({'put': 'approve_announcement'}),
             name='approve-announcement'),
        path('announcement_moderation_reject/<int:pk>',
             views.AnnouncementModerationAdminView.as_view({'patch': 'reject_announcement'}),
             name='reject-announcement'),
        path('request_to_chest_create', views.RequestToChestCreateView.as_view(), name='request-to-chest-create'),
        path('request_to_chest', views.RequestToChestViewSet.as_view({'get': 'list'}), name='request-to-chest-list'),
        path('request_to_chest/<int:pk>', views.RequestToChestViewSet.as_view({'get': 'retrieve'})),
        path('request_to_chest_approve/<int:pk>', views.RequestToChestViewSet.as_view({'put': 'approve_request'}),
             name='request-to-chest-approve'),
        path('request_to_chest_reject/<int:pk>', views.RequestToChestViewSet.as_view({'delete': 'destroy'})),
        path('news', views.NewsViewSet.as_view({'get': 'list'})),
        path('news/<int:pk>', views.NewsViewSet.as_view({'get': 'retrieve'})),
        path('news_create', views.NewsViewSet.as_view({'post': 'create'})),
        path('news_update/<int:pk>', views.NewsViewSet.as_view({'put': 'update', 'patch': 'partial_update'})),
        path('news_delete/<int:pk>', views.NewsViewSet.as_view({'delete': 'destroy'})),
        path('document', views.DocumentViewSet.as_view({'get': 'list'})),
        path('document/<int:pk>', views.DocumentViewSet.as_view({'get': 'retrieve'})),
        path('document_create', views.DocumentViewSet.as_view({'post': 'create'})),
        path('document_update/<int:pk>', views.DocumentViewSet.as_view({'put': 'update', 'patch': 'partial_update'})),
        path('document_delete/<int:pk>', views.DocumentViewSet.as_view({'delete': 'destroy'})),
        # ADVANTAGES
        path('advantage', views.AdvantageViewSet.as_view({'get': 'list'})),
        path('advantage_update/<int:pk>', views.AdvantageViewSet.as_view({'put': 'update'})),
        path('advantage_create', views.AdvantageViewSet.as_view({'post': 'create'})),
        path('advantage_delete/<int:pk>', views.AdvantageViewSet.as_view({'delete': 'destroy'})),
        path('residential_complex_add_advantage', views.ResidentialAdvantagesViewSet.as_view({'post': 'create'})),
        path('residential_complex_delete_advantage', views.ResidentialAdvantagesViewSet.as_view({'delete': 'destroy'})),
    ]
