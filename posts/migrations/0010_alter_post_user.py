# Generated by Django 3.2 on 2021-06-13 07:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_backgroundimage_profileimage'),
        ('posts', '0009_alter_image_metadata'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='user.student'),
        ),
    ]
