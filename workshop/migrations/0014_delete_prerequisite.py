# Generated by Django 3.2 on 2021-12-09 00:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workshop', '0013_workshop_prerequisites'),
    ]

    operations = [
        migrations.DeleteModel(
            name='PreRequisite',
        ),
    ]
