from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.response import Response

from building.models import Building
from building.serializers import BuildingSerializer, BuildingReadSerializer, BuildingHistorySerializer
from building_post.models import BuildingPost
from building_post.serializers import BuildingPostSerializer


class BuildingViewSet(viewsets.ModelViewSet):
    serializer_class = BuildingSerializer
    parser_classes = (MultiPartParser,)
    queryset = Building.objects.filter(is_enabled=True)

    def get_serializer_class(self):
        if self.request.method in ('GET',):
            self.parser_classes = (JSONParser,)
            return BuildingReadSerializer
        return BuildingSerializer

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    def perform_update(self, serializer):
        serializer.save(creator=self.request.user)

    def perform_destroy(self, instance):
        instance.is_enabled = False
        instance.save()

    @action(methods=['get', 'post'], detail=True)
    def posts(self, request, pk=None):
        if request.method == 'GET':
            if not pk:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            post_list = BuildingPost.objects.filter(is_enabled=True,
                                                    building_id=pk)
            serializer = BuildingPostSerializer(post_list, many=True)
            return Response(serializer.data)


class BuildingHistoryViewSet(viewsets.ModelViewSet):
    serializer_class = BuildingHistorySerializer
