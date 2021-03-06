# Generated by Django 3.2 on 2021-05-23 16:57

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_auto_20210523_2144'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='user_id',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='like',
            old_name='user_id',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='post',
            old_name='user_id',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='share',
            old_name='user_id',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='vote',
            old_name='user_id',
            new_name='user',
        ),
        migrations.AlterField(
            model_name='comment',
            name='id',
            field=models.UUIDField(default=uuid.UUID('4bd3389d-9e36-4b8a-9f0a-684e73063b3a'), editable=False, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='image',
            name='id',
            field=models.UUIDField(default=uuid.UUID('34ade849-9915-4c31-9941-8a1bf2c0a3b2'), editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='like',
            name='id',
            field=models.UUIDField(default=uuid.UUID('29ec2467-491e-4ad5-8f35-1cc55860fe14'), editable=False, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='id',
            field=models.UUIDField(default=uuid.UUID('e1e7ac9c-d836-4b48-a30c-f03f313f2d08'), editable=False, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='share',
            name='id',
            field=models.UUIDField(default=uuid.UUID('a6a020a1-0473-4e47-9665-efb6778b2ca4'), editable=False, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='vote',
            name='id',
            field=models.UUIDField(default=uuid.UUID('58f445c1-c7b7-4516-a6f0-f7cac3598fcd'), editable=False, primary_key=True, serialize=False, unique=True),
        ),
    ]
