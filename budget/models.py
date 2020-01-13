import datetime
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    icon = models.CharField(max_length=10, default="i")
    sign = models.IntegerField(default=-1)

    def __str__(self):
        return self.name


class Budget(models.Model):
    id = models.AutoField(primary_key=True)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    date = models.DateField(default=datetime.date.today)
    category = models.ForeignKey(
        Category, related_name="category", on_delete=models.PROTECT
    )
    note = models.TextField(default=None, blank=True)


class BudgetSummary(Budget):
    class Meta:
        proxy = True
        verbose_name = "Budget Summary"
        verbose_name_plural = "Budget Summaries"


class Tower(models.Model):
    LEVEL = [
        ("dzialka", "dzialka"),
        ("formalnosci", "formalnosci"),
        ("stan0", "stan 0 - fundament"),
        ("stan1", "stan surowy otwarty"),
        ("stan2", "stan surowy zamknięty"),
        ("stan3", "wykonczenie"),
        ("stan4", "zakonczenie budowy"),
    ]
    STATUS = [
        ("open", "open"),
        ("planned", "planned"),
        ("set", "set"),
        ("in_progress", "in progress"),
        ("finished", "finished"),
        ("on hold", "on hold"),
    ]
    PERCENTAGE = [
        (0, "0 %"),
        (1, "10 %"),
        (20, "20 %"),
        (30, "30 %"),
        (40, "40 %"),
        (50, "50 %"),
        (60, "60 %"),
        (70, "70 %"),
        (80, "80 %"),
        (90, "90 %"),
        (100, "100 %"),
    ]
    level = models.CharField(choices=LEVEL, max_length=128)
    task = models.CharField(max_length=128)
    # $$$
    plan_amount_material = models.DecimalField(
        max_digits=8, decimal_places=2, default=0
    )
    plan_amount_work = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    real_amount = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    # ***
    added_date = models.DateField(default=datetime.date.today)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    # ???
    note = models.TextField(default=None, blank=True)
    status = models.CharField(choices=STATUS, max_length=128, default="open")
    percentage = models.IntegerField(choices=PERCENTAGE)

    def __str__(self):
        return self.task

    def days_last(self):
        if self.end_date and self.start_date:
            diff = f"{self.end_date - self.start_date}".split(",")
            if len(diff) == 1:
                return "1 day"
            return diff[0]
        else:
            return "N/A"

    @property
    def color(self):
        colors = {
            "open": "gray",
            "planned": "purple",
            "set": "orange",
            "in_progress": "yellow",
            "finished": "green",
            "on hold": "blue",
        }
        return colors[self.status]
