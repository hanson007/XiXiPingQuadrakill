# Generated by Django 4.1 on 2022-08-28 01:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('permissions', '0011_alter_routes2_routes1'),
    ]

    operations = [
        migrations.AlterField(
            model_name='routes1',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all url granted to each of their groups.', to='auth.group', verbose_name='角色'),
        ),
        migrations.CreateModel(
            name='ApiPermission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='接口名称')),
                ('url', models.CharField(max_length=128, verbose_name='url')),
                ('method', models.CharField(max_length=128, verbose_name='请求方式')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all url granted to each of their groups.', to='auth.group', verbose_name='角色')),
            ],
            options={
                'db_table': 'api_permission',
            },
        ),
    ]
