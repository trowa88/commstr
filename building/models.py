from django.db import models

from core.models import TimeStampedEnabledModel, Cities


class Building(TimeStampedEnabledModel):
    city = models.ForeignKey(Cities, on_delete=models.DO_NOTHING, null=False)
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    img_src = models.ImageField(null=True)

    class Meta:
        db_table = 'building'

    def __str__(self):
        return self.name
