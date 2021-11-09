# Generated by Django 3.2.9 on 2021-11-08 23:55

from django.db import migrations
import django_fsm


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0013_alter_volunteer_account'),
    ]

    operations = [
        migrations.AddField(
            model_name='volunteer',
            name='state',
            field=django_fsm.FSMIntegerField(choices=[(0, 'New'), (10, 'Pending'), (20, 'Confirmed')], default=0),
        ),
    ]