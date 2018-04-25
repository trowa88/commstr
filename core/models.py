from django.db import models


class TimeStampedEnabledModel(models.Model):
    is_enabled = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Country(models.Model):
    country_code = models.CharField(max_length=2)
    country_name = models.CharField(max_length=255)

    class Meta:
        db_table = 'country'

    def __str__(self):
        return f'{self.country_code}: {self.country_name}'


class States(models.Model):
    country = models.ForeignKey('Country', on_delete=models.DO_NOTHING, null=True)
    state_code = models.CharField(max_length=20)
    state_name = models.CharField(max_length=255)

    class Meta:
        db_table = 'states'

    def __str__(self):
        return f'{self.pk}: {self.state_name}'


class Cities(models.Model):
    country = models.ForeignKey('Country', on_delete=models.DO_NOTHING, null=True)
    state = models.ForeignKey('States', on_delete=models.DO_NOTHING, null=True)
    city_name = models.CharField(max_length=255)
    city_name_ascii = models.CharField(max_length=255)
    latitude = models.DecimalField(max_digits=15, decimal_places=5)
    longitude = models.DecimalField(max_digits=15, decimal_places=5)
    timezone_name = models.ForeignKey('Timezone', on_delete=models.DO_NOTHING, null=True)

    class Meta:
        db_table = 'cities'

    def __str__(self):
        return self.city_name_ascii


class Timezone(models.Model):
    country = models.ForeignKey('Country', on_delete=models.DO_NOTHING, null=True)
    timezone_name = models.CharField(max_length=255)
    gmt_offset = models.DecimalField(max_digits=10, decimal_places=3)
    dst_offset = models.DecimalField(max_digits=10, decimal_places=3)
    raw_offset = models.DecimalField(max_digits=10, decimal_places=3)

    class Meta:
        db_table = 'timezone'

    def __str__(self):
        return f'timezone_name: {self.timezone_name}, gmt: {self.gmt_offset}, ' \
               f'dst: {self.dst_offset}, raw: {self.raw_offset}'
