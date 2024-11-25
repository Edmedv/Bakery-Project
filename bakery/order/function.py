from order.models import Drivers, Clients, Products, Orders


def select_drivers():
    return Drivers.objects.all()


def select_clients():
    return Clients.objects.all()


def select_products():
    return Products.objects.all()


def output_orders(today, orders):
    orders['clients'] = {}
    orders['products'] = []
    for o in Orders.objects.filter(date=today).values('client_id', 'product_id', 'number'):
        if o['product_id'] not in orders['products']:
            orders['products'].append(o['product_id'])
            index = orders['products'].index(o['product_id'])

        if o['client_id'] not in orders['clients']:
            orders['clients'][o['client_id']] = []

        orders['clients'][o['client_id']].insert(index, o['number'])
    print(orders)
    return orders


def output_drivers(today, drivers):
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

    return drivers


def add_orders(req):
    for r in req:
        print(r)
        if r != 'csrfmiddlewaretoken':
            rep = r.split(':')
            print(rep)
            client_now = rep[0]
            client_id = Clients.objects.filter(client=client_now).first()

            product_now = rep[1]
            product_id = Products.objects.filter(product=product_now).first()
            driver_now = Clients.objects.filter(client=client_now).first().driver_id.id
            driver_id = Drivers.objects.filter(id=driver_now).first()
            extra = Orders.objects.filter(driver_id=driver_id,
                                          client_id=client_id,
                                          product_id=product_id)

            if req[f'{r}'] == '' and not extra:
                Orders.objects.create(driver_id=driver_id,
                                      client_id=client_id,
                                      product_id=product_id)
                continue
            if req[f'{r}'] != '' and not extra:
                Orders.objects.create(driver_id=driver_id,
                                      client_id=client_id,
                                      product_id=product_id,
                                      number=req[f'{r}'])
                continue

            if extra and req[f'{r}'] != '':
                Orders.objects.filter(driver_id=driver_id,
                                      client_id=client_id,
                                      product_id=product_id).update(number=req[f'{r}'])

