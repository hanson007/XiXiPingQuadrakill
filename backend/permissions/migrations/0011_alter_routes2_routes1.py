# Generated by Django 4.1 on 2022-08-25 01:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('permissions', '0010_routes2_routes1'),
    ]

    operations = [
        migrations.AlterField(
            model_name='routes2',
            name='routes1',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='permissions.routes1'),
        ),
    ]
