# Generated by Django 5.0.13 on 2025-04-11 02:53

import django.contrib.gis.db.models.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('donnees', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='equipementsql',
            name='geom',
            field=django.contrib.gis.db.models.fields.PointField(blank=True, null=True, srid=4326),
        ),
    ]
