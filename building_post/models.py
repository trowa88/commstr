from django.db import models

from building.models import Building
from core.models import TimeStampedEnabledModel


class AbstractBuildingPost(TimeStampedEnabledModel):
    building = models.ForeignKey(Building, on_delete=models.DO_NOTHING, null=False)
    creator = models.ForeignKey('users.User', on_delete=models.DO_NOTHING, null=False)
    title = models.CharField(max_length=100)
    content = models.TextField()

    class Meta:
        abstract = True


class BuildingPost(AbstractBuildingPost):
    class Meta:
        db_table = 'building_post'
        ordering = ['-updated']

    def __str__(self):
        return self.title


class BuildingPostHistory(AbstractBuildingPost):
    building_post = models.ForeignKey('BuildingPost', on_delete=models.DO_NOTHING, null=False)

    class Meta:
        db_table = 'building_post_history'
        ordering = ['-pk']
