# Generated by Django 4.1 on 2022-08-20 04:36

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('permissions', '0003_alter_profile_table'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='create_time',
            field=models.DateTimeField(default=datetime.datetime(2022, 8, 20, 4, 36, 59, 762695), verbose_name='创建时间'),
        ),
    ]
