from django_filters import rest_framework as filters

from building.models import Announcement


class AnnouncementFilter(filters.FilterSet):
    price = filters.RangeFilter()

    class Meta:
        model = Announcement
        fields = ['appointment', 'room_quantity', 'price', 'area', 'layout', 'living_condition']
