from rest_framework import serializers

from building.models import Building
from core.serializers import CitySerializer


class BuildingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Building
        fields = ('id', 'city', 'name', 'desc', 'address', 'img_src')
        read_only_fields = ('id',)


class BuildingReadSerializer(BuildingSerializer):
    city = CitySerializer(read_only=True)
