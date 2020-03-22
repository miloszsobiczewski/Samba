# Generated by Django 2.2.1 on 2019-12-27 15:46

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("budget", "0004_auto_20191124_1217")]

    operations = [
        migrations.CreateModel(
            name="Tower",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "level",
                    models.CharField(
                        choices=[
                            ("dzialka", "dzialka"),
                            ("formalnosci", "formalnosci"),
                            ("stan0", "stan 0 - fundament"),
                            ("stan1", "stan surowy otwarty"),
                            ("stan2", "stan surowy zamknięty"),
                            ("stan3", "wykonczenie"),
                            ("stan4", "zakonczenie budowy"),
                        ],
                        max_length=128,
                    ),
                ),
                ("task", models.CharField(max_length=128)),
                (
                    "plan_amount_material",
                    models.DecimalField(decimal_places=2, default=0, max_digits=8),
                ),
                (
                    "plan_amount_work",
                    models.DecimalField(decimal_places=2, default=0, max_digits=8),
                ),
                (
                    "real_amount",
                    models.DecimalField(decimal_places=2, default=0, max_digits=8),
                ),
                ("added_date", models.DateField(default=datetime.date.today)),
                ("start_date", models.DateField(blank=True, null=True)),
                ("end_date", models.DateField(blank=True, null=True)),
                ("note", models.TextField(blank=True, default=None)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("open", "open"),
                            ("planned", "planned"),
                            ("set", "set"),
                            ("in progress", "in progress"),
                            ("finished", "finished"),
                            ("on hold", "on hold"),
                        ],
                        max_length=128,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="BudgetSummary",
            fields=[],
            options={
                "verbose_name": "Budget Summary",
                "verbose_name_plural": "Budget Summaries",
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("budget.budget",),
        ),
    ]