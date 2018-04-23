from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from building.models import Building
from building.serializers import BuildingSerializer


class BuildingViewSet(viewsets.ModelViewSet):
    serializer_class = BuildingSerializer
    permission_classes = [IsAuthenticated]
    queryset = Building.objects.all()
