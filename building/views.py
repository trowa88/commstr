from rest_framework import viewsets
from rest_framework.parsers import JSONParser, MultiPartParser

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

    def perform_destroy(self, instance):
        instance.is_enabled = False
        instance.save()
