# Generated by Django 3.2 on 2021-06-17 19:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_remove_organization_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='name',
            field=models.TextField(default='', max_length=50),
        ),
    ]
