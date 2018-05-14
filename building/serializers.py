from rest_framework import serializers
from rest_framework.relations import StringRelatedField

from building.models import Building, BuildingPost
from core.serializers import CitySerializer


class BuildingSerializer(serializers.ModelSerializer):
    img_src = serializers.ImageField(read_only=False)

    class Meta:
        model = Building
        fields = ('slug', 'city', 'name', 'desc', 'address', 'img_src')
        read_only_fields = ('is_enabled',)

    def to_internal_value(self, data):
        pass


class BuildingReadSerializer(BuildingSerializer):
    city = CitySerializer(read_only=True)

    class Meta(BuildingSerializer.Meta):
        fields = (
            'id', 'slug', 'city', 'name', 'desc', 'address', 'img_src',
            'created', 'updated'
        )


class BuildingPostSerializer(serializers.ModelSerializer):
    creator = StringRelatedField()

    class Meta:
        model = BuildingPost
        fields = ('building', 'creator', 'title', 'content', 'created', 'updated')
