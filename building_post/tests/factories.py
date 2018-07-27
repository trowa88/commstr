import factory

from building.tests.factories import BuildingFactory
from jwt_drf.users.tests.factories import UserFactory


class BuildingPostFactory(factory.django.DjangoModelFactory):
    building = factory.SubFactory(BuildingFactory)
    creator = factory.SubFactory(UserFactory)
    title = factory.sequence(lambda s: f'title-{s}')
    content = factory.sequence(lambda s: f'content-{s}')

    class Meta:
        model = 'building_post.BuildingPost'
