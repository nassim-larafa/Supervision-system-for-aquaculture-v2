# Generated by Django 5.0.2 on 2024-05-15 11:07

import django.contrib.gis.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_myproject_cage_node_data_parcelle_node_parc_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='polygonModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('geom', django.contrib.gis.db.models.fields.PolygonField(srid=4326)),
            ],
        ),
    ]
