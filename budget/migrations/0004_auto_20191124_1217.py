# Generated by Django 2.2.1 on 2019-11-24 12:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budget', '0003_auto_20191124_1108'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='icon',
            field=models.CharField(default='i', max_length=10),
        ),
        migrations.AlterField(
            model_name='category',
            name='sign',
            field=models.IntegerField(default=-1),
        ),
    ]
