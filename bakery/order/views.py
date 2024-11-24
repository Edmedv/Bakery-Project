from django.shortcuts import render
import datetime
import numpy as np
from order.models import Drivers, Clients, Products, Orders
import pandas as pd


# Create your views here.

def select_drivers():
    return Drivers.objects.all()

def select_clients():
    return Clients.objects.all()

def select_products():
    return Products.objects.all()


def order(request):
    if request.method == 'POST':
        for r in request.POST:
            if r != 'csrfmiddlewaretoken':
                req = r.split(':')
                client_now = req[0]
                client_id = Clients.objects.filter(client=client_now).first()

                product_now = req[1]
                product_id = Products.objects.filter(product=product_now).first()

                driver_now = Clients.objects.filter(client=client_now).first().driver_id.id
                driver_id = Drivers.objects.filter(id=driver_now).first()

                if request.POST[f'{r}'] == '':
                    Orders.objects.create(driver_id=driver_id,
                                          client_id=client_id,
                                          product_id=product_id)
                else:
                    Orders.objects.create(driver_id=driver_id,
                                          client_id=client_id,
                                          product_id=product_id,
                                          number=request.POST[f'{r}'])

    clients = select_clients()
    products = select_products()
    return render(request, 'order/order.html',
                  {'clients': clients, 'products': products})


def add_data(request):
    if request.method == 'POST':
        if 'driver' in request.POST and request.POST['driver'] != '':
            Drivers.objects.create(driver=request.POST['driver'])

        if 'client' in request.POST and 'drive' in request.POST and request.POST['client'] != '':
            drive = Drivers.objects.filter(driver=request.POST['drive'])[0]
            Clients.objects.create(client=request.POST['client'], driver_id=drive)

        if 'product' in request.POST and request.POST['product'] != '':
            Products.objects.create(product=request.POST['product'])

    drivers = Drivers.objects.all()
    return render(request, 'order/add_data.html', {'drivers': drivers})


def print_orders(request):
    if request.method == 'POST':
        today = request.POST['date_order']
    else:
        today = datetime.date.today().isoformat()
    drivers = {}
    orders = {}
    orders['clients'] = []
    orders['products'] = {}
    sum_client = []

    for o in Orders.objects.filter(date=today).values('driver_id', 'client_id', 'product_id', 'number'):
        if o['driver_id'] not in drivers:
            drivers[o['driver_id']] = {}
            drivers[o['driver_id']]['clients'] = []
            drivers[o['driver_id']]['products'] = {}

        if o['client_id'] not in drivers[o['driver_id']]['clients']:
            drivers[o['driver_id']]['clients'].append(o['client_id'])
        index = drivers[o['driver_id']]['clients'].index(o['client_id'])

        if o['product_id'] not in drivers[o['driver_id']]['products']:
            drivers[o['driver_id']]['products'][o['product_id']] = []

        drivers[o['driver_id']]['products'][o['product_id']].insert(index, o['number'])

    for key, value in drivers.items():
        for key2, value2 in value['products'].items():
            value2.append(sum(value2))

    for o in Orders.objects.filter(date=today).values('client_id', 'product_id', 'number'):
        if o['client_id'] not in orders['clients']:
            orders['clients'].append(o['client_id'])
            index = orders['clients'].index(o['client_id'])

        if o['product_id'] not in orders['products']:
            orders['products'][o['product_id']] = []

        orders['products'][o['product_id']].insert(index, o['number'])

    for key, value in orders['products'].items():
        if sum_client == []:
            sum_client = value
        sum_client = np.add(sum_client, value).tolist()
        value.append(sum(value))
    print(sum_client)

    sum_cli = sum(sum_client)

    return render(request, 'order/print_order.html',
                  {'drivers': drivers, 'orders': orders, 'today': today,
                   'sum_client': sum_client, 'sum_cli': sum_cli})


