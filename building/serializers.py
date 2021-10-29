from datetime import date

from generic_relations.relations import GenericRelatedField
from generic_relations.serializers import GenericModelSerializer
from rest_framework import serializers

from building.models import ResidentialComplex, Announcement, AnnouncementShot, Promotion, Complaint


class ResidentialComplexListSerializer(serializers.ModelSerializer):

    class Meta:
        model = ResidentialComplex
        fields = ('id', 'name', 'price_for_meter', 'min_area', 'max_area', 'frame_quantity', 'address')


class ResidentialComplexSerializer(serializers.ModelSerializer):

    class Meta:
        model = ResidentialComplex
        fields = '__all__'
        extra_kwargs = {
            "created": {"read_only": True},
            "updated": {"read_only": True},
        }


class AnnouncementListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Announcement
        fields = ('id', 'price', 'room_quantity', 'photo', 'created', 'address')


class GallerySerializer(serializers.ModelSerializer):

    class Meta:
        model = AnnouncementShot
        fields = ('id', 'image', 'announcement')


class AnnouncementSerializer(serializers.ModelSerializer):
    shots = GallerySerializer(many=True, read_only=True)

    class Meta:
        model = Announcement
        fields = "__all__"


class PromotionRetrieveSerializer(serializers.ModelSerializer):

    class Meta:
        model = Promotion
        fields = "__all__"


class PromotionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Promotion
        exclude = ('price', )
        extra_kwargs = {
            "finished": {"read_only": True}
        }

    def create(self, validated_data):
        promotion = Promotion(**validated_data)
        promotion.finished = date.today().replace(month=1 if date.today().month//12 == 1 else date.today().month + 1)
        promotion.price = promotion.calculate_price()
        promotion.save()
        return promotion

    def update(self, instance, validated_data):
        for validated_field, value in validated_data.items():
            setattr(instance, validated_field, value)
        instance.price = instance.calculate_price()
        instance.save()
        return instance


class ComplaintSerializer(serializers.ModelSerializer):

    class Meta:
        model = Complaint
        exclude = ('rejected', 'user')

    def create(self, validated_data):
        complaint = Complaint(**validated_data)
        complaint.user = self.context['request'].user
        complaint.save()
        return complaint


class ComplaintRejectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Complaint
        fields = ('rejected',)
