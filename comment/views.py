from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from comment.models import BuildingPostComment
from comment.serializers import BuildingPostCommentSerializer, BuildingPostCommentReadSerializer


class BuildingPostCommentViewSet(viewsets.ModelViewSet):
    serializer_class = BuildingPostCommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

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
