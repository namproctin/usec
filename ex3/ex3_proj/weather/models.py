from django.db import models


class Weather(models.Model):
    location = models.CharField(max_length=50)
    data = models.TextField()
