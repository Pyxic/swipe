from django.urls import path

from account import views

urlpatterns = [
    path('role_list', views.RoleListView.as_view()),
    path('client', views.ClientViewSet.as_view({'get': 'list'})),
    path('client/<int:pk>', views.ClientViewSet.as_view({'get': 'retrieve'})),
    path('client_update/<int:pk>', views.ClientViewSet.as_view({'put': 'update', 'patch': 'partial_update'})),
    path('notary', views.NotaryViewSet.as_view({'get': 'list'})),
    path('notary/<int:pk>', views.NotaryViewSet.as_view({'get': 'retrieve'})),
    path('notary_update/<int:pk>', views.NotaryUpdateView.as_view()),
    path('notary_delete/<int:pk>', views.NotaryDestroyView.as_view()),
    path('developer', views.ClientViewSet.as_view({'get': 'list'})),
    path('developer/<int:pk>', views.ClientViewSet.as_view({'get': 'retrieve'})),
    path('developer_update/<int:pk>', views.ClientViewSet.as_view({'put': 'update', 'patch': 'partial_update'})),
    # path('client_create', views.ClientCreateView.as_view()),
]