from rest_framework import viewsets

from building_post.models import BuildingPost
from building_post.serializers import BuildingPostSerializer


class BuildingPostViewSet(viewsets.ModelViewSet):
    serializer_class = BuildingPostSerializer
    queryset = BuildingPost.objects.filter(is_enabled=True)

    def perform_destroy(self, instance):
        instance.is_enabled = False
        instance.save()
