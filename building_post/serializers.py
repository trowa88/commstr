from rest_framework import serializers
from rest_framework.relations import StringRelatedField

from building_post.models import BuildingPost


class BuildingPostSerializer(serializers.ModelSerializer):
    creator = StringRelatedField()

    class Meta:
        model = BuildingPost
        fields = ('building', 'creator', 'title', 'content', 'created', 'updated')
