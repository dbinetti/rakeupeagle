# Generated by Django 3.1.4 on 2020-12-14 17:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_auto_20201213_1557'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='volunteer',
            name='recipient',
        ),
        migrations.AddField(
            model_name='volunteer',
            name='assignment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='assignments', to='app.recipient'),
        ),
    ]
