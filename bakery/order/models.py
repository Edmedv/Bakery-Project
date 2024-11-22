from django.db import models
from datetime import date

# Create your models here.


class Drivers(models.Model):
    driver = models.CharField(max_length=50, unique=True, null=False)



class Clients(models.Model):
    client = models.CharField(max_length=50, unique=True, null=False)
    driver_id = models.ForeignKey('Drivers', on_delete=models.PROTECT)



class Products(models.Model):
    product = models.CharField(max_length=50, unique=True, null=False)


class Orders(models.Model):
    driver_id = models.ForeignKey('Drivers', on_delete=models.PROTECT, null=True)
    client_id = models.ForeignKey('Clients', on_delete=models.PROTECT, null=True)
    product_id = models.ForeignKey('Products', on_delete=models.PROTECT, null=True)
    number = models.IntegerField(default=0)
    date = models.DateField(auto_now_add=True)