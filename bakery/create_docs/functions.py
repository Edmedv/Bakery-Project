from order.models import Orders

def add_order_for_xml(orders, t):
    for order in Orders.objects.filter(date=t):
        if order.client.name not in orders['клиенты/продукты']:
            orders['клиенты/продукты'].append(order.client.name)

        if f'{order.product.name}' not in orders:
            orders[f'{order.product.name}'] = []

        orders[f'{order.product.name}'].append(order.number)

    return orders


def create_context_for_docx(client_id, today, context):
    o = Orders.objects.filter(date=today, client=client_id).first()
    context['client'] = o.client.name
    context['standart'] = o.client.str_standart
    context['orders'] = {}
    vivod = Orders.objects.filter(date=today, client=client_id)
    for i, order in zip(range(1, len(vivod) +  1), vivod):
        if f'{order.product.name}' not in context['orders']:
            context['orders'][f'{order.product.name}'] = []
        context['orders'][f'{order.product.name}'].append(i)
        context['orders'][f'{order.product.name}'].append(order.product.name)
        context['orders'][f'{order.product.name}'].append(order.number)
        context['orders'][f'{order.product.name}'].append('шт')
        context['orders'][f'{order.product.name}'].append(int(order.product.price))
        context['orders'][f'{order.product.name}'].append(order.product.price * order.number)
    print(context)
    return context
