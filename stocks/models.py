from django.db import models

# Create your models here.
class Stock(models.Model):
    symbol = models.CharField(max_length=30, unique=True)
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name