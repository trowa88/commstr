import factory

from building_post.tests.factories import BuildingPostFactory
from jwt_drf.users.tests.factories import UserFactory


class BuildingPostCommentFactory(factory.django.DjangoModelFactory):
    building_post = factory.SubFactory(BuildingPostFactory)
    creator = factory.SubFactory(UserFactory)
    content = factory.sequence(lambda s: f'content-{s}')

    class Meta:
        model = 'comment.BuildingPostComment'
