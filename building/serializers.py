from django.core.exceptions import PermissionDenied
from rest_framework import serializers

from building.models import Building, BuildingHistory
from core.serializers import CitySerializer


class BuildingSerializer(serializers.ModelSerializer):
    img_src = serializers.ImageField(use_url=True, required=False)
    creator = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Building
        fields = (
            'city',
            'name',
            'desc',
            'address',
            'img_src',
            'creator',
        )
        read_only_fields = (
            'is_enabled',
        )

    def update(self, instance, validated_data):
        if self.context['request'].user != instance.creator:
            raise PermissionDenied()
        new_instance = super(BuildingSerializer, self).update(instance, validated_data)
        BuildingHistory.objects.create(
            building=instance,
            city=instance.city,
            name=instance.name,
            desc=instance.desc,
            address=instance.address,
            img_src=instance.img_src,
            creator=instance.creator
        )
        return new_instance


class BuildingReadSerializer(BuildingSerializer):
    city = CitySerializer(read_only=True)

    class Meta(BuildingSerializer.Meta):
        fields = (
            'id',
            'city',
            'name',
            'desc',
            'address',
            'img_src',
            'is_enabled',
            'creator',
            'created',
            'updated',
        )


class BuildingHistorySerializer(serializers.ModelSerializer):
    img_src = serializers.ImageField(use_url=True, required=False)

    class Meta:
        model = BuildingHistory
        fields = (
            'building',
            'city',
            'name',
            'desc',
            'address',
            'img_src',
            'creator',
        )
        read_only_fields = (
            'is_enabled',
        )
