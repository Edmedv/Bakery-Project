from django.shortcuts import render
import datetime
import numpy as np
from order.models import Drivers, Clients, Products, Orders
from .function import *

# Create your views here.


def order(request):
    today = datetime.date.today().isoformat()

    if request.method == 'POST':
        add_orders(request.POST)

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

    drivers = select_drivers()
    return render(request, 'order/add_data.html', {'drivers': drivers})


def print_orders(request):
    if request.method == 'POST':
        today = request.POST['date_order']
    else:
        today = datetime.date.today().isoformat()
    drivers = {}
    orders = {}
    sum_client = []

    output_drivers(today, drivers)

    for key, val in drivers.items():
        for key2, val2 in val['products'].items():
            val2.append(sum(val2))

    output_orders(today, orders)

    for key, value in orders['clients'].items():
        if sum_client == []:
            for i in range(len(value)):
                sum_client.append(0)
        sum_client = np.add(sum_client, value).tolist()
        value.append(sum(value))

    sum_cli = sum(sum_client)

    return render(request, 'order/print_order.html',
                  {'drivers': drivers, 'orders': orders, 'today': today,
                   'sum_client': sum_client, 'sum_cli': sum_cli})
