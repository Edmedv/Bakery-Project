from django.db import models

# Create your models here.


class Drivers(models.Model):
    driver = models.CharField(max_length=50, unique=True, null=False)



class Clients(models.Model):
    client = models.CharField(max_length=50, unique=True, null=False)
    driver_id = models.ForeignKey('Drivers', on_delete=models.PROTECT)



class Products(models.Model):
    product = models.CharField(max_length=50, unique=True, null=False)


class Orders(models.Model):
    driver_id = models.ForeignKey('Drivers', to_field='driver', on_delete=models.PROTECT)
    client_id = models.ForeignKey('Clients', to_field='client', on_delete=models.PROTECT)
    product_id = models.ForeignKey('Products', to_field='product',on_delete=models.PROTECT)
    number = models.IntegerField(default=0)
    date = models.DateField(auto_now_add=True)