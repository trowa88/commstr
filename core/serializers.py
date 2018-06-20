from rest_framework import serializers
from rest_framework.relations import StringRelatedField

from core.models import Country, States, Cities, Timezone


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ('country_code', 'country_name')


class StatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = States
        fields = ('state_code', 'state_name')


class TimezoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Timezone
        fields = ('timezone_name', 'gmt_offset', 'dst_offset', 'raw_offset')


class CitySerializer(serializers.ModelSerializer):
    country = CountrySerializer(read_only=True)
    state = StatesSerializer(read_only=True)
    timezone_name = TimezoneSerializer(read_only=True)

    class Meta:
        model = Cities
        fields = ('country', 'state', 'city_name', 'city_name_ascii',
                  'latitude', 'longitude', 'timezone_name')
