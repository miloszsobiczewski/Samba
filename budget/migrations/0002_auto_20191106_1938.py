# Generated by Django 2.2.1 on 2019-11-06 19:38

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ("budget", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="budget",
            name="date",
            field=models.DateField(
                default=datetime.datetime(2019, 11, 6, 19, 38, 4, 905475, tzinfo=utc)
            ),
        ),
    ]
