from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from building_post.models import BuildingPost
from building_post.serializers import BuildingPostSerializer, BuildingPostReadSerializer


class BuildingPostViewSet(viewsets.ModelViewSet):
    serializer_class = BuildingPostSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        return BuildingPost.objects.filter(
            is_enabled=True,
            building=self.kwargs['building_pk']
        )

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
