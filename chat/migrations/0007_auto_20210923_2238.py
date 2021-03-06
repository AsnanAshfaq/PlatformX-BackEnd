# Generated by Django 3.2 on 2021-09-23 17:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0006_channelmodel'),
    ]

    operations = [
        migrations.RenameField(
            model_name='chat',
            old_name='timestamp',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='message',
            old_name='timestamp',
            new_name='created_at',
        ),
        migrations.AddField(
            model_name='chat',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='message',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
