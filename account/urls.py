from django.urls import path

from account import views

urlpatterns = [
    path('role_list', views.RoleListView.as_view()),
    path('admin', views.AdminViewSet.as_view({'get': 'list'})),
    path('admin/<int:pk>', views.AdminViewSet.as_view({'get': 'retrieve'})),
    path('client', views.ClientViewSet.as_view({'get': 'list'})),
    path('client/<int:pk>', views.ClientViewSet.as_view({'get': 'retrieve'})),
    path('client_update/<int:pk>', views.ClientViewSet.as_view({'put': 'update', 'patch': 'partial_update'})),
    path('client_subscription/<int:pk>', views.ClientUpdateSubscriptionView.as_view()),
    path('notary', views.NotaryViewSet.as_view({'get': 'list'})),
    path('notary/<int:pk>', views.NotaryViewSet.as_view({'get': 'retrieve'})),
    path('notary_update/<int:pk>', views.NotaryUpdateView.as_view()),
    path('notary_delete/<int:pk>', views.NotaryDestroyView.as_view()),
    path('developer', views.DeveloperViewSet.as_view({'get': 'list'})),
    path('developer/<int:pk>', views.DeveloperViewSet.as_view({'get': 'retrieve'})),
    path('developer_update/<int:pk>', views.DeveloperViewSet.as_view({'put': 'update', 'patch': 'partial_update'})),
    path('change_ban_status/<int:pk>', views.ChangeBanStatus.as_view()),
    path('user_filter', views.UserFilterViewSet.as_view({'get': 'list'})),
    path('user_filter/<int:pk>', views.UserFilterViewSet.as_view({'get': 'retrieve'})),
    path('user_filter_update/<int:pk>', views.UserFilterViewSet.as_view({'put': 'update', 'patch': 'partial_update'})),
    path('user_filter_create', views.UserFilterViewSet.as_view({'post': 'create'})),
    path('user_filter_delete/<int:pk>', views.UserFilterViewSet.as_view({'delete': 'destroy'})),
]
