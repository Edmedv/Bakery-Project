from django.db import models

# Create your models here.


class Drivers(models.Model):
    driver = models.CharField(max_length=50, unique=True, null=False)


class Clients(models.Model):
    client = models.CharField(max_length=50, unique=True, null=False)
    driver_id = models.ForeignKey('Drivers', on_delete=models.PROTECT)


class Products(models.Model):
    product = models.CharField(max_length=50, unique=True, null=False)