from rest_framework import serializers

from comment.models import BuildingPostComment, BuildingPostCommentHistory


class BuildingPostCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = BuildingPostComment
        fields = (
            'building_post',
            'content',
        )

    def update(self, instance, validated_data):
        if self.context['request'].user != instance.creator:
            raise PermissionDenied()
        new_instance = super(BuildingPostCommentSerializer, self).update(instance, validated_data)
        BuildingPostCommentHistory.objects.create(
            building_post_comment=instance,
            building_post=instance.building_post,
            creator=instance.creator,
            content=instance.content
        )
        return new_instance


class BuildingPostCommentReadSerializer(BuildingPostCommentSerializer):
    class Meta(BuildingPostCommentSerializer.Meta):
        fields = (
            'id',
            'building_post',
            'creator',
            'content',
            'created',
            'updated',
            'is_enabled',
        )
