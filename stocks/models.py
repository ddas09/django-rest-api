from django.db import models

# Create your models here.
class Stock(models.Model):
    symbol = models.TextField(unique=True)
    name = models.TextField(unique=True)

    class Meta:
        managed = False
        db_table = 'stocks'

    def __str__(self):
        return self.name