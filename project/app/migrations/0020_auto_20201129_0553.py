# Generated by Django 3.1.3 on 2020-11-29 13:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0019_recipient_addresss'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recipient',
            name='address',
        ),
        migrations.RemoveField(
            model_name='recipient',
            name='geo',
        ),
    ]
