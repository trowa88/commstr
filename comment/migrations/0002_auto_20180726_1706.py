# Generated by Django 2.0.4 on 2018-07-26 08:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='buildingpostcomment',
            name='building',
        ),
        migrations.RemoveField(
            model_name='buildingpostcommenthistory',
            name='building',
        ),
    ]
