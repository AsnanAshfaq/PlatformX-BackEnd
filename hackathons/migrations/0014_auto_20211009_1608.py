# Generated by Django 3.2 on 2021-10-09 11:08

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hackathons', '0013_auto_20211009_1603'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='built_with',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.TextField(default='', max_length=25), blank=True, default=list, size=None),
        ),
        migrations.AlterField(
            model_name='project',
            name='links',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.URLField(default=''), blank=True, default=list, size=None),
        ),
    ]
