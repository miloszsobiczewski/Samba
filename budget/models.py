import uuid
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=50)
    sign = models.IntegerField()


class Budget(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    amount = models.CharField(max_length=100)
    date = models.CharField(max_length=200)
    category = models.ForeignKey(Category)
    note = models.TextField()
