from rest_framework import serializers

from building.models import Building
from core.serializers import CitySerializer


class BuildingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Building
        fields = ('id', 'city', 'name', 'address', 'img_src')


class BuildingReadSerializer(BuildingSerializer):
    city = CitySerializer(read_only=True)
