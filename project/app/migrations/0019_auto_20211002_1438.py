# Generated by Django 3.2.7 on 2021-10-02 20:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0018_auto_20211002_0758'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recipient',
            name='address',
        ),
        migrations.RemoveField(
            model_name='recipient',
            name='email',
        ),
        migrations.RemoveField(
            model_name='recipient',
            name='familiar_name',
        ),
        migrations.RemoveField(
            model_name='recipient',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='recipient',
            name='formal_name',
        ),
        migrations.RemoveField(
            model_name='recipient',
            name='greeting_name',
        ),
        migrations.RemoveField(
            model_name='recipient',
            name='last_name',
        ),
        migrations.RemoveField(
            model_name='recipient',
            name='middle_name',
        ),
        migrations.RemoveField(
            model_name='recipient',
            name='name',
        ),
        migrations.RemoveField(
            model_name='recipient',
            name='nick_name',
        ),
        migrations.RemoveField(
            model_name='recipient',
            name='phone',
        ),
        migrations.RemoveField(
            model_name='recipient',
            name='prefix',
        ),
        migrations.RemoveField(
            model_name='recipient',
            name='suffix',
        ),
    ]
