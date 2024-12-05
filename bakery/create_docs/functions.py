from order.models import Orders
from num2words import num2words
import os


def add_order_for_xml(orders, t):
    for order in Orders.objects.filter(date=t):
        if order.client.name not in orders['клиенты/продукты']:
            orders['клиенты/продукты'].append(order.client.name)

        if f'{order.product.name}' not in orders:
            orders[f'{order.product.name}'] = []

        orders[f'{order.product.name}'].append(order.number)

    return orders


def create_context_for_docx_standart(client_id, today, context):
    o = Orders.objects.filter(date=today, client=client_id).first()
    context['client'] = o.client.name
    context['standart'] = o.client.str_standart
    context['orders'] = {}
    vivod = Orders.objects.filter(date=today, client=client_id)
    for i, order in zip(range(1, len(vivod) +  1), vivod):
        if f'{order.product.name}' not in context['orders']:
            context['orders'][f'{order.product.name}'] = []
        data_ext = [
            i, order.product.name, order.number, 'шт', f'{int(order.product.price)}-00', order.product.price * order.number
        ]
        context['orders'][f'{order.product.name}'].extend(data_ext)
        context['sum_all'] += int(order.product.price * order.number)
    context['len'] = len(context['orders'])
    context['rub'] = num2words(int(context['sum_all'] // 1), lang='ru')
    context['kop'] = '00' if int((context['sum_all'] % 1) * 100) == 0 else int((context['sum_all'] % 1) * 100)
    return context


def create_context_for_docx_torg12(client_id, today, context):
    o = Orders.objects.filter(date=today, client=client_id).first()
    context['client'] = o.client.name
    context['str_torg12'] = o.client.str_torg12
    context['orders'] = {}
    context['orders2'] = {}
    vivod = Orders.objects.filter(date=today, client=client_id)
    num = 0
    sum_prod1 = 0
    sum_prod2 = 0
    sum_oll1 = 0
    sum_oll2 = 0
    sum_products = 0
    sum_all = 0
    for i, order in zip(range(1, len(vivod) +  1), vivod):
        data_ext = [
            i, f'{order.product.name} ({order.product.weight / 1000} кг)', '', 'шт', '796', '', '', '', '',
            f'{order.number}.000',
            f'{int(order.product.price)}-{int(order.product.price % 1 * 100) if int(order.product.price % 1 * 100) != 0 else "00"}',
            f'{int(order.number * order.product.price)}-{int((order.number * order.product.price) % 1 * 100) if int((order.number * order.product.price) % 1 * 100) != 0 else "00"}',
            '-', '-',
            f'{int(order.number * order.product.price)}-{int((order.number * order.product.price) % 1 * 100) if int((order.number * order.product.price) % 1 * 100) != 0 else "00"}'
        ]

        sum_products += order.number
        sum_all += order.number * order.product.price

        if i <= 8:
            if f'{i}' not in context['orders']:
                context['orders'][f'{i}'] = []
            context['orders'][f'{i}'].extend(data_ext)
            sum_prod1 += order.number
            sum_oll1 += order.number * order.product.price

        if i > 8:
            if f'{i}' not in context['orders2']:
                context['orders2'][f'{i}'] = []
            context['orders2'][f'{i}'].extend(data_ext)
            sum_prod2 += order.number
            sum_oll2 += order.number * order.product.price

        num = i

    if num < 8:
        for r in range(8 - num, 9):
            context['orders'][f'{r}'] = ['' for n in range(15)]
        context['orders2']['null'] = ['' for n in range(15)]

    context['sum_prod1'] = sum_prod1
    context['sum_prod2'] = sum_prod2
    context['sum_products'] = sum_products
    context['sum_all'] = f'{int(sum_all)}-{sum_all % 1 * 100 if sum_all % 1 * 100 != 0 else "00"}'
    context['sum_oll1'] = f'{int(sum_oll1)}-{sum_oll1 % 1 * 100 if sum_oll1 % 1 * 100 != 0 else "00"}'
    context['sum_oll2'] = f'{int(sum_oll2)}-{sum_oll2 % 1 * 100 if sum_oll2 % 1 * 100 != 0 else "00"}'
    context['chis'] = num2words(num, lang='ru')
    return context