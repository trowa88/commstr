from django.db import models


class Building(models.Model):
    name = models.CharField(max_length=50)
    is_enabled = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'building'

    def __str__(self):
        return self.name
