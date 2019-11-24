from django.db import models


class Connection(models.Model):
    name = models.CharField(max_length=32)
    config = models.TextField()
    user = models.CharField(max_length=16)
    password = models.CharField(max_length=16)
    # todo : add synchro date
