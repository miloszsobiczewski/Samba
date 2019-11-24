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
    category = models.ForeignKey(Category, related_name="category", on_delete=models.PROTECT)
    note = models.TextField(default=None, blank=True)
