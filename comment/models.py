from django.db import models

from core.models import TimeStampedEnabledModel


class AbstractBuildingPostComment(TimeStampedEnabledModel):
    building = models.ForeignKey('building.Building', on_delete=models.DO_NOTHING, null=False)
    building_post = models.ForeignKey('building_post.BuildingPost', on_delete=models.DO_NOTHING, null=False)
    creator = models.ForeignKey('users.User', on_delete=models.DO_NOTHING, null=False)
    content = models.CharField(max_length=500)

    class Meta:
        abstract = True


class BuildingPostComment(AbstractBuildingPostComment):
    class Meta:
        db_table = 'building_post_comment'
        ordering = ['-updated']

    def __str__(self):
        return self.content


class BuildingPostCommentHistory(AbstractBuildingPostComment):
    building_post_comment = models.ForeignKey('BuildingPostComment', on_delete=models.DO_NOTHING, null=False)

    class Meta:
        db_table = 'building_post_comment_history'
        ordering = ['-pk']
