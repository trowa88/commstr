from rest_framework import viewsets

from building_post.models import BuildingPost
from building_post.serializers import BuildingPostSerializer, BuildingPostReadSerializer


class BuildingPostViewSet(viewsets.ModelViewSet):
    serializer_class = BuildingPostSerializer
    queryset = BuildingPost.objects.filter(is_enabled=True)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return BuildingPostReadSerializer
        return BuildingPostSerializer

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    def perform_update(self, serializer):
        serializer.save(creator=self.request.user)

    def perform_destroy(self, instance):
        instance.is_enabled = False
        instance.save()
