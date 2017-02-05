from django.db import models


class User(models.Model):
    created = models.DateTimeField(auto_now_add=True)  # time server receives values
    email = models.CharField(max_length=100, blank=False, unique=True)
    name = models.CharField(max_length=100, blank=False)
    password = models.CharField(max_length=64, blank=False)


class DataPoint(models.Model):
    user = models.ForeignKey(User, related_name='datapoints')
    created = models.DateTimeField(auto_now_add=True)  # time server receives values
    time = models.DateTimeField(auto_now_add=True)  # time sensor generates values
    tag = models.CharField(max_length=100, blank=True, default='')
    temperature = models.CharField(max_length=10)
    humidity = models.CharField(max_length=10)
    orientation = models.CharField(max_length=100)


    class Meta:
        ordering = ['id']