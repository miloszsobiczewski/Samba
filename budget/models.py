import uuid
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    icon = models.CharField(max_length=10)
    sign = models.IntegerField()

    def __str__(self):
        return self.name


class Budget(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    amount = models.DecimalField(max_digits=4, decimal_places=2)
    date = models.DateField()
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    note = models.TextField(default=None, blank=True)
