# Generated by Django 3.2 on 2021-11-23 17:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workshop', '0004_alter_workshop_description'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='prerequisite',
            name='list',
        ),
        migrations.AddField(
            model_name='prerequisite',
            name='description',
            field=models.TextField(blank=True),
        ),
    ]