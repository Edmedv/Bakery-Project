from order.models import Drivers, Clients, Products, Orders


def select_drivers():
    return Drivers.objects.all()


def select_clients():
    return Clients.objects.all()


def select_products():
    return Products.objects.all()


def output_orders(today, orders):
    for order in Orders.objects.filter(date=today):
        if order.product.name not in orders['products']:
            orders['products'].append(order.product.name)
            index = orders['products'].index(order.product.name)

        if f'{order.client.name}' not in orders['clients']:
            orders['clients'][f'{order.client.name}'] = []

        orders['clients'][f'{order.client.name}'].insert(index, order.number)

    for key, value in orders['clients'].items():
        value.append(sum(value))

    return orders


def output_drivers(today, drivers):
    for order in Orders.objects.filter(date=today):
        if f'{order.driver}' not in drivers:
            drivers[f'{order.driver}'] = {}
            drivers[f'{order.driver}']['products'] = {}
            drivers[f'{order.driver}']['clients'] = []

        if order.client.name not in drivers[f'{order.driver}']['clients']:
            drivers[f'{order.driver}']['clients'].append(order.client.name)
            index = drivers[f'{order.driver}']['clients'].index(order.client.name)

        if f'{order.product.name}' not in drivers[f'{order.driver}']['products']:
            drivers[f'{order.driver}']['products'][f'{order.product.name}'] = []
        drivers[f'{order.driver}']['products'][f'{order.product.name}'].insert(index, order.number)

    for key, value in drivers.items():
        for key2, value2 in value['products'].items():
            value2.append(sum(value2))

    return drivers


def add_orders(req, today):
    for r in req:
        if r != 'csrfmiddlewaretoken':
            rep = r.split(':')
            client_now = rep[0]
            client_id = Clients.objects.filter(name=client_now).first()

            product_now = rep[1]
            product_id = Products.objects.filter(name=product_now).first()
            driver_now = Clients.objects.filter(name=client_now).first().driver
            driver_id = Drivers.objects.filter(name=driver_now).first()

            if req[f'{r}'] == '':
                Orders.objects.create(driver=driver_id,
                                      client=client_id,
                                      product=product_id)

            if req[f'{r}'] != '':
                Orders.objects.create(driver=driver_id,
                                      client=client_id,
                                      product=product_id,
                                      number=req[f'{r}'])

