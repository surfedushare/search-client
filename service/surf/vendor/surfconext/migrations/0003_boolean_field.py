# Generated by Django 3.2.3 on 2021-06-03 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('surfconext', '0002_auto_20200706_1141'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datagoalpermission',
            name='is_allowed',
            field=models.BooleanField(null=True, verbose_name='is allowed'),
        ),
    ]
