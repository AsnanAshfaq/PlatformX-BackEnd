# Generated by Django 3.2 on 2021-09-30 13:19

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0007_organization_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='incorporation_date',
            field=models.DateField(default=datetime.date.today),
        ),
    ]
