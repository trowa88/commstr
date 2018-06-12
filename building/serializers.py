from rest_framework import serializers

from building.models import Building
from core.serializers import CitySerializer


class BuildingSerializer(serializers.ModelSerializer):
    img_src = serializers.ImageField(use_url=True, required=False)
    creator = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Building
        fields = ('city', 'name', 'desc', 'address', 'img_src', 'creator',)
        read_only_fields = ('is_enabled',)


class BuildingReadSerializer(BuildingSerializer):
    city = CitySerializer(read_only=True)

    class Meta(BuildingSerializer.Meta):
        fields = (
            'id', 'city', 'name', 'desc', 'address', 'img_src',
            'is_enabled', 'creator',
            'created', 'updated',
        )
