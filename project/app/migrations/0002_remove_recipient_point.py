# Generated by Django 4.1.2 on 2022-11-04 17:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recipient',
            name='point',
        ),
    ]
