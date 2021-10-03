# Generated by Django 3.2.7 on 2021-10-02 12:29

from django.conf import settings
import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion
import django_fsm
import hashid_field.field
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_auto_20210930_2035'),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', hashid_field.field.HashidAutoField(alphabet='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890', min_length=7, prefix='', primary_key=True, serialize=False)),
                ('state', django_fsm.FSMIntegerField(choices=[(0, 'New')], default=0)),
                ('name', models.CharField(blank=True, default='', max_length=100)),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None)),
                ('email', models.EmailField(blank=True, default='', max_length=254)),
                ('address', models.CharField(blank=True, default='', max_length=512)),
                ('place', models.CharField(blank=True, default='', max_length=255)),
                ('is_precise', models.BooleanField(default=False)),
                ('point', django.contrib.gis.db.models.fields.PointField(blank=True, null=True, srid=4326)),
                ('geocode', models.JSONField(blank=True, null=True)),
                ('notes', models.TextField(blank=True, default='', max_length=2000)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='account', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]