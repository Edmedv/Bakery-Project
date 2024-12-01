from django.db import models

# Create your models here.


class Drivers(models.Model):
    name = models.CharField(max_length=50, unique=True, null=False)

    def __str__(self):
        return self.name



class Clients(models.Model):
    name = models.CharField(max_length=50, unique=True, null=False)
    str_torg12 = models.CharField(max_length=200, unique=True)
    str_standart = models.CharField(max_length=200, unique=True)
    driver = models.ForeignKey('Drivers', on_delete=models.SET_NULL, null=True)


class Products(models.Model):
    name = models.CharField(max_length=50, unique=True, null=False)
    price = models.FloatField(null = False)
    weight = models.FloatField(null =False)


class Orders(models.Model):
    driver = models.ForeignKey('Drivers', on_delete=models.DO_NOTHING)
    client = models.ForeignKey('Clients', on_delete=models.DO_NOTHING)
    product = models.ForeignKey('Products',on_delete=models.DO_NOTHING)
    number = models.IntegerField(default=0)
    date = models.DateField(auto_now_add=True)


class Invoices(models.Model):
    standart = models.IntegerField()
    torg12 = models.IntegerField()