import coreapi
from rest_framework import viewsets, status
from rest_framework.parsers import MultiPartParser, JSONParser
from rest_framework.response import Response

from building.models import Building
from building.serializers import BuildingSerializer, BuildingReadSerializer


class BuildingViewSet(viewsets.ModelViewSet):
    serializer_class = BuildingSerializer
    parser_classes = (MultiPartParser,)
    queryset = Building.objects.filter(is_enabled=True)

    def get_serializer_class(self):
        if self.request.method in ('GET',):
            self.parser_classes = (JSONParser,)
            return BuildingReadSerializer
        return BuildingSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_enabled = False
        return Response(status=status.HTTP_204_NO_CONTENT)
