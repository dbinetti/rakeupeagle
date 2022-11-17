# Generated by Django 4.1.3 on 2022-11-05 15:04

from django.db import migrations
import django_fsm


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_remove_recipient_point'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='state',
            field=django_fsm.FSMIntegerField(choices=[(-20, 'Cancelled'), (-10, 'Excluded'), (0, 'New'), (10, 'Included'), (20, 'Confirmed'), (30, 'Checked-In')], default=0),
        ),
    ]