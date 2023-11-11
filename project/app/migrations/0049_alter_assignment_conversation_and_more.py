# Generated by Django 4.2.7 on 2023-11-11 06:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0048_remove_conversation_user_assignment_conversation_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignment',
            name='conversation',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='assignment', to='app.conversation'),
        ),
        migrations.AlterField(
            model_name='recipient',
            name='conversation',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='recipient', to='app.conversation'),
        ),
        migrations.AlterField(
            model_name='team',
            name='conversation',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='team', to='app.conversation'),
        ),
    ]