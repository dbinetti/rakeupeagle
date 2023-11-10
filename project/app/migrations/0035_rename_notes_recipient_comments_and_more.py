# Generated by Django 4.2.7 on 2023-11-10 05:31

import django.contrib.gis.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0034_yard_phone'),
    ]

    operations = [
        migrations.RenameField(
            model_name='recipient',
            old_name='notes',
            new_name='comments',
        ),
        migrations.RemoveField(
            model_name='recipient',
            name='geocode',
        ),
        migrations.RemoveField(
            model_name='recipient',
            name='is_precise',
        ),
        migrations.RemoveField(
            model_name='recipient',
            name='place',
        ),
        migrations.AddField(
            model_name='recipient',
            name='point',
            field=django.contrib.gis.db.models.fields.PointField(blank=True, null=True, srid=4326),
        ),
        migrations.AddField(
            model_name='yard',
            name='name',
            field=models.CharField(blank=True, default='', help_text='Your full name.', max_length=100),
        ),
    ]