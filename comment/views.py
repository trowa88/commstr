from rest_framework import viewsets

from comment.models import BuildingPostComment
from comment.serializers import BuildingPostCommentSerializer, BuildingPostCommentReadSerializer


class BuildingPostCommentViewSet(viewsets.ModelViewSet):
    serializer_class = BuildingPostCommentSerializer

    def get_queryset(self):
        return BuildingPostComment.objects.filter(
            is_enabled=True,
            building_post=self.kwargs['post_pk']
        )

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return BuildingPostCommentReadSerializer
        return BuildingPostCommentSerializer

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    def perform_update(self, serializer):
        serializer.save(creator=self.request.user)

    def perform_destroy(self, instance):
        instance.is_enabled = False
        instance.save()
