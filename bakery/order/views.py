import re

from dateutil.utils import today
from django.shortcuts import render
import datetime
import numpy as np
from order.forms import ProductForm, ClientsForm, DriversForm
from order.models import Products, Clients, Drivers, Orders
from .function import *

# Create your views here.


def order(request):
    today = datetime.date.today()
    if request.method == 'POST':
        extra = Orders.objects.filter(date=today)
        if extra:
            extra.delete()
        add_orders(request.POST, today)

    if Orders.objects.filter(date=today):
        pass
    clients = select_clients()
    products = select_products()
    return render(request, 'order/order.html',
              {'clients': clients, 'products': products})


def add_data(request):
    if request.method == 'POST':
        print(request.POST)
        if 'drivers' in request.POST:
            drivers_form = DriversForm(request.POST)
            if drivers_form.is_valid():
                drivers_form.save()

        if 'clients' in request.POST:
            clients_form = ClientsForm(request.POST)
            if clients_form.is_valid():
                clients_form.save()

        if 'products' in request.POST:
            products_form = ProductForm(request.POST)
            if products_form.is_valid():
                products_form.save()


        if 'update_driver' in request.POST:
            if 'delete_driver' in request.POST:
                old_driver = list(request.POST.values())[1]
                print(old_driver)
                Drivers.objects.filter(name=old_driver).delete()
            else:
                old_driver = list(request.POST.keys())[2]
                new_driver = list(request.POST.values())[1]
                Drivers.objects.filter(name=old_driver).update(name=new_driver)

        if 'update_client_name' in request.POST:
            old_client = list(request.POST.keys())[5]
            new_driver = Drivers.objects.filter(name=request.POST['update_client_driver']).first()
            Clients.objects.filter(name=old_client).update(name=request.POST['update_client_name'],
                                                           str_torg12=request.POST['update_client_torg12'],
                                                           str_standart=request.POST['update_client_standart'],
                                                           driver=new_driver)

        if 'update_product_name' in request.POST:
            if 'delete_product' in request.POST:
                old_product = list(request.POST.values())[1]
                Products.objects.filter(name=old_product).delete()

            old_product = list(request.POST.keys())[4]
            Products.objects.filter(name=old_product).update(name=request.POST['update_product_name'],
                                                           price=request.POST['update_product_price'],
                                                           weight=request.POST['update_product_weight'])


    products = select_products()
    clients = select_clients()
    drivers = select_drivers()

    products_form = ProductForm()
    clients_form = ClientsForm()
    drivers_form = DriversForm()
    return render(request, 'order/add_data.html', {'drivers_form': drivers_form,
                                                   'products_form': products_form,
                                                   'clients_form': clients_form,
                                                   'products': products,
                                                   'clients': clients,
                                                   'drivers': drivers})


def print_orders(request):
    if request.method == 'POST':
        today = request.POST['date_order']
    else:
        today = datetime.date.today().isoformat()

    drivers = {}
    output_drivers(today, drivers)

    orders = {}
    orders['clients'] = {}
    orders['products'] = []
    output_orders(today, orders)

    sum_client = []
    for key, value in orders['clients'].items():
        if len(sum_client) == 0:
            sum_client = [0 for v in range(len(value))]
        sum_client = [x + y for x, y in zip(sum_client, value)]
    print(drivers)

    return render(request, 'order/print_order.html', {'orders': orders,
                                                                          'drivers': drivers,
                                                                          'today': today,
                                                                          'sum_client': sum_client})