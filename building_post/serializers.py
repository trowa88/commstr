from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied
from rest_framework.relations import StringRelatedField

from building.serializers import BuildingSerializer
from building_post.models import BuildingPost, BuildingPostHistory


class BuildingPostSerializer(serializers.ModelSerializer):
    creator = StringRelatedField()

    class Meta:
        model = BuildingPost
        fields = (
            'building',
            'creator',
            'title',
            'content',
        )

    def update(self, instance, validated_data):
        if self.context['request'].user != instance.creator:
            raise PermissionDenied()
        new_instance = super(BuildingPostSerializer, self).update(instance, validated_data)
        BuildingPostHistory.objects.create(
            building_post=instance,
            building=instance.building,
            creator=instance.creator,
            title=instance.title,
            content=instance.content
        )
        return new_instance


class BuildingPostReadSerializer(BuildingPostSerializer):
    building = BuildingSerializer(many=False)

    class Meta(BuildingPostSerializer.Meta):
        fields = (
            'id',
            'building',
            'creator',
            'title',
            'content',
            'is_enabled',
            'created',
            'updated',
        )
