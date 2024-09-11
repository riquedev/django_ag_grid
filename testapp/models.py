from django.db import models


class TestModel(models.Model):
    value = models.IntegerField(default=1)
