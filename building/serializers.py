from rest_framework import serializers

from building.models import Building
from core.serializers import CitySerializer


class BuildingSerializer(serializers.ModelSerializer):
    city = CitySerializer(many=False, read_only=True)

    class Meta:
        model = Building
        fields = ('name', 'city', 'address', 'img_src')
