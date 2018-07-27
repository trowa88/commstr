import factory

from core.tests.factories import CitiesFactory
from jwt_drf.users.tests.factories import UserFactory


class BuildingFactory(factory.django.DjangoModelFactory):
    city = factory.SubFactory(CitiesFactory)
    name = factory.sequence(lambda s: f'building-{s}')
    desc = factory.sequence(lambda s: f'desc-{s}')
    address = factory.sequence(lambda s: f'address-{s}')
    img_src = factory.django.ImageField()
    creator = factory.SubFactory(UserFactory)

    class Meta:
        model = 'building.Building'
        django_get_or_create = (
            'name',
            'city',
        )
