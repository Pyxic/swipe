from datetime import date

from generic_relations.relations import GenericRelatedField
from generic_relations.serializers import GenericModelSerializer
from rest_framework import serializers

from account.models import User
from building.models import ResidentialComplex, Announcement, AnnouncementShot, Promotion, Complaint, RequestToChest, \
    News, Document


class ResidentialComplexListSerializer(serializers.ModelSerializer):

    class Meta:
        model = ResidentialComplex
        fields = ('id', 'name', 'price_for_meter', 'min_area', 'max_area', 'frame_quantity', 'address', 'user')


class ResidentialComplexSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='email', read_only=True)

    class Meta:
        model = ResidentialComplex
        fields = '__all__'
        extra_kwargs = {
            "created": {"read_only": True},
            "updated": {"read_only": True},
        }


class PromotionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Promotion
        fields = "__all__"
        extra_kwargs = {
            "finished": {"read_only": True},
            "price": {"read_only": True},
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


class AnnouncementListSerializer(serializers.ModelSerializer):
    promotion = PromotionSerializer(read_only=True)

    class Meta:
        model = Announcement
        fields = ('id', 'price', 'room_quantity', 'photo', 'created', 'address', 'user', 'promotion')


class GallerySerializer(serializers.ModelSerializer):

    class Meta:
        model = AnnouncementShot
        fields = ('id', 'image', 'announcement')


class AnnouncementSerializer(serializers.ModelSerializer):
    shots = GallerySerializer(many=True, read_only=True)
    in_favorites = serializers.SlugRelatedField(slug_field='email', read_only=True, many=True)
    promotion = PromotionSerializer(read_only=True)

    class Meta:
        model = Announcement
        fields = "__all__"
        extra_kwargs = {
            'is_draft': {"read_only": True}
        }


class PromotionRetrieveSerializer(serializers.ModelSerializer):

    class Meta:
        model = Promotion
        fields = "__all__"


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


class AnnouncementModerationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Announcement
        fields = ('reject_message',)

    def update(self, instance, validated_data):
        for validated_field, value in validated_data.items():
            setattr(instance, validated_field, value)
        instance.reject = True
        instance.save()
        return instance


class RequestToChestSerializer(serializers.ModelSerializer):

    class Meta:
        model = RequestToChest
        fields = "__all__"

    def validate(self, data):
        residential_complex = data.get('residential_complex')
        announcement = data.get('announcement')
        if announcement.frame > residential_complex.frame_quantity:
            raise serializers.ValidationError("frame of flat must be less than frame quantity of complex")
        if announcement.section > residential_complex.section_quantity:
            raise serializers.ValidationError("section of flat must be less than section quantity of complex")
        if announcement.level > residential_complex.level_quantity:
            raise serializers.ValidationError("level of flat must be less than level quantity of complex")
        return data


class NewsSerializer(serializers.ModelSerializer):

    class Meta:
        model = News
        fields = "__all__"


class DocumentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Document
        fields = "__all__"
