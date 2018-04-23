from rest_framework import serializers

from core.models import Country, States, Cities, Timezone


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ('country_code', 'country_name')


class StatesSerializer(serializers.ModelSerializer):
    country = CountrySerializer(many=False, read_only=True)

    class Meta:
        model = States
        fields = ('country', 'state_code', 'state_name')


class TimezoneSerializer(serializers.ModelSerializer):
    country = CountrySerializer(many=False, read_only=True)

    class Meta:
        model = Timezone
        fields = ('country', 'timezone_name', 'gmt_offset', 'dst_offset', 'raw_offset')


class CitySerializer(serializers.ModelSerializer):
    country = CountrySerializer(many=False, read_only=True)
    state = StatesSerializer(many=False, read_only=True)
    timezone_name = TimezoneSerializer(many=False, read_only=True)

    class Meta:
        model = Cities
        fields = ('country', 'state', 'city_name', 'city_name_ascii',
                  'latitude', 'longitude', 'timezone_name')
