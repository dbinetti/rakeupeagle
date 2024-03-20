# Generated by Django 4.2.7 on 2023-11-15 19:06

from django.db import migrations
import django_fsm


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_alter_team_state'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignment',
            name='state',
            field=django_fsm.FSMIntegerField(choices=[(-20, 'Failed'), (-10, 'Cancelled'), (0, 'New'), (20, 'Confirmed'), (30, 'Checked-In'), (40, 'Started'), (50, 'Finished')], default=0),
        ),
    ]