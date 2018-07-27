import factory
from factory.fuzzy import FuzzyDecimal


class CountryFactory(factory.django.DjangoModelFactory):
    country_code = factory.sequence(lambda s: f'K{s}')
    country_name = factory.sequence(lambda s: f'대한민국-{s}')

    class Meta:
        model = 'core.Country'
        django_get_or_create = (
            'country_code',
        )


class StatesFactory(factory.django.DjangoModelFactory):
    country = factory.SubFactory(CountryFactory)
    state_code = factory.sequence(lambda s: f'SEOUL-{s}')
    state_name = factory.sequence(lambda s: f'서울-{s}')

    class Meta:
        model = 'core.States'
        django_get_or_create = (
            'country',
            'state_code',
        )


class TimezoneFactory(factory.django.DjangoModelFactory):
    country = factory.SubFactory(CountryFactory)
    timezone_name = factory.sequence(lambda s: f'timezone-{s}')
    gmt_offset = FuzzyDecimal(99.9, precision=3)
    dst_offset = FuzzyDecimal(99.9, precision=3)
    raw_offset = FuzzyDecimal(99.9, precision=3)

    class Meta:
        model = 'core.Timezone'
        django_get_or_create = (
            'country',
            'timezone_name',
        )


class CitiesFactory(factory.django.DjangoModelFactory):
    country = factory.SubFactory(CountryFactory)
    state = factory.SubFactory(StatesFactory)
    city_name = factory.sequence(lambda s: f'city-{s}')
    city_name_ascii = factory.sequence(lambda s: f'city_ascii-{s}')
    latitude = FuzzyDecimal(50.0)
    longitude = FuzzyDecimal(89.2)

    class Meta:
        model = 'core.Cities'
        django_get_or_create = (
            'country',
            'state',
            'city_name',
        )
