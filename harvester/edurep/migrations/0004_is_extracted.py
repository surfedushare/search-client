# Generated by Django 3.2.12 on 2022-04-19 11:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('edurep', '0003_json_field'),
    ]

    operations = [
        migrations.AddField(
            model_name='edurepoaipmh',
            name='is_extracted',
            field=models.BooleanField(default=False),
        ),
    ]