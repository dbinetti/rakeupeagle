# Generated by Django 4.2.7 on 2023-11-14 16:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0056_rename_actual_team_adults_remove_assignment_bags_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='conversation',
            name='user',
        ),
        migrations.RemoveField(
            model_name='message',
            name='content',
        ),
        migrations.RemoveField(
            model_name='message',
            name='conversation',
        ),
        migrations.RemoveField(
            model_name='messagearchive',
            name='user',
        ),
        migrations.RemoveField(
            model_name='participant',
            name='conversation',
        ),
        migrations.RemoveField(
            model_name='receipt',
            name='conversation',
        ),
        migrations.RemoveField(
            model_name='receipt',
            name='message',
        ),
        migrations.RemoveField(
            model_name='receipt',
            name='participant',
        ),
        migrations.DeleteModel(
            name='Content',
        ),
        migrations.DeleteModel(
            name='Conversation',
        ),
        migrations.DeleteModel(
            name='Message',
        ),
        migrations.DeleteModel(
            name='MessageArchive',
        ),
        migrations.DeleteModel(
            name='Participant',
        ),
        migrations.DeleteModel(
            name='Receipt',
        ),
    ]
