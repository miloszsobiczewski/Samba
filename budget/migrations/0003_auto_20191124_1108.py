# Generated by Django 2.2.1 on 2019-11-24 11:08

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("budget", "0002_auto_20191106_1938"),
    ]

    operations = [
        migrations.AlterField(
            model_name="budget",
            name="date",
            field=models.DateField(default=datetime.date.today),
        ),
    ]
