# Generated by Django 4.2.7 on 2023-11-13 15:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0049_alter_assignment_conversation_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignment',
            name='recipient',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='assignments', to='app.recipient'),
        ),
        migrations.AddField(
            model_name='assignment',
            name='team',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='assignments', to='app.team'),
        ),
    ]
