from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from building.models import Building
from building.serializers import BuildingSerializer, BuildingReadSerializer


class BuildingViewSet(viewsets.ModelViewSet):
    serializer_class = BuildingSerializer
    permission_classes = [IsAuthenticated]
    queryset = Building.objects.all()

    def get_serializer_class(self):
        if self.request.method in ('GET',):
            return BuildingReadSerializer
        return BuildingSerializer
