# Generated by Django 3.2 on 2021-12-11 00:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0015_auto_20211211_0518'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='github',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='student',
            name='linked_in',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='student',
            name='portfolio',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='student',
            name='twitter',
            field=models.TextField(blank=True, default=''),
        ),
    ]
