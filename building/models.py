from django.db import models

from core.models import TimeStampedEnabledModel, Cities


class Building(TimeStampedEnabledModel):
    city = models.ForeignKey(Cities, on_delete=models.DO_NOTHING, null=False)
    name = models.CharField(max_length=50)
    desc = models.CharField(max_length=100, blank=True)
    address = models.CharField(max_length=50)
    img_src = models.ImageField(upload_to='buildings/', default=None)
    creator = models.ForeignKey('users.User', on_delete=models.DO_NOTHING, null=False,
                                default=None)

    class Meta:
        db_table = 'building'
        ordering = ['-updated']

    def __str__(self):
        return self.name
