# Generated by Django 2.2.20 on 2021-05-21 09:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_sync_lock'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Arrangement',
        ),
        migrations.RemoveField(
            model_name='collection',
            name='dataset',
        ),
        migrations.RemoveField(
            model_name='document',
            name='dataset',
        ),
        migrations.RemoveField(
            model_name='elasticindex',
            name='dataset',
        ),
    ]
