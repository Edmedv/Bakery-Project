from django.shortcuts import render
from docxtpl import DocxTemplate
from datetime import datetime, date
from .functions import *
import pandas as pd
from order.models import Orders
import os


# Create your views here.

def create_dir(str):
    t = datetime.today()
    now_date = [t.year, t.month, t.day]
    basedir = f'create_docs/templates/docx/{str}/'
    for dir in now_date:
        basedir += f'{dir}/'
        try:
            os.mkdir(f'{basedir}')
        except:
            pass


def add_xml():
    t = datetime.today()
    now_date = [t.year, t.month, t.day]
    basedir = 'create_docs/templates/xml/'
    for dir in now_date:
        basedir += f'{dir}/'
        try:
            os.mkdir(f'{basedir}')
        except:
            pass
    orders = {}
    orders['клиенты/продукты'] = []
    add_order_for_xml(orders, t)
    df = pd.DataFrame(orders)
    df.to_excel(f'{basedir}/Заявка.xlsx', sheet_name='Заявка', index=False)


def add_docx_standart():
    t = datetime.today()
    today = date.today()
    now_date = [t.year, t.month, t.day]
    day_now = now_date[2] if now_date[2] // 10 > 0 else f'0{now_date[2]}'
    t = datetime.today()
    now_date = [t.year, t.month, t.day]
    basedir = f'create_docs/templates/docx/standart/'
    for dir in now_date:
        basedir += f'{dir}/'
        try:
            os.mkdir(f'{basedir}')
        except:
            pass
    for order in Orders.objects.filter(date=t).values('client').distinct():
        doc = DocxTemplate("create_docs/templates/patterns/pattern_standart.docx")

        context = {}
        context['sum_all'] = 0
        context['today'] = f'{day_now}.{now_date[1]}.{now_date[0] % 100}'
        client_id = list(order.values())[0]
        create_context_for_docx_standart(client_id, today, context)
        doc.render(context)
        name_doc = f'{context['client']}.docx'
        doc.save(f'{basedir}/{name_doc}')


def add_docx_torg12():
    t = datetime.today()
    today = date.today()
    now_date = [t.year, t.month, t.day]
    day_now = now_date[2] if now_date[2] // 10 > 0 else f'0{now_date[2]}'
    t = datetime.today()
    now_date = [t.year, t.month, t.day]
    basedir = f'create_docs/templates/docx/torg12/'
    for dir in now_date:
        basedir += f'{dir}/'
        try:
            os.mkdir(f'{basedir}')
        except:
            pass
    for order in Orders.objects.filter(date=t).values('client').distinct():
        doc = DocxTemplate("create_docs/templates/patterns/pattern_torg12.docx")

        context = {}
        context['sum_all'] = 0
        context['today'] = f'{day_now}.{now_date[1]}.{now_date[0] % 100}'
        client_id = list(order.values())[0]
        create_context_for_docx_torg12(client_id, today, context)

        doc.render(context)
        name_doc = f'{context['client']}.docx'
        doc.save(f'{basedir}/{name_doc}')


def create_docx(request):
    create_dir('standart')
    create_dir('torg12')
    t = datetime.today()
    today = date.today()
    now_date = [t.year, t.month, t.day]
    dir_date = f'{now_date[0]}/{now_date[1]}/{now_date[2]}'
    if request.method == 'POST':
        if 'standart' in request.POST:
            add_docx_standart()
        if 'torg12' in request.POST:
            add_docx_torg12()
        else:
            req = list(request.POST)[1].split(':')
            dir_os = 'C://Users/EdMedved/PycharmProjects/ProjectBakery/bakery/create_docs/templates/docx/'
            if req[0] == 'open_standart':
                os.startfile(f'{dir_os}standart/{dir_date}/{req[1]}')
            if req[0] == 'open_torg12':
                os.startfile(f'{dir_os}torg12/{dir_date}/{req[1]}')

    clients = []
    for c in Orders.objects.filter(date=today):
        if c.client.name not in clients:
            clients.append(c.client.name)
    standart = os.listdir(f'create_docs/templates/docx/standart/{dir_date}')
    torg12 = os.listdir(f'create_docs/templates/docx/torg12/{dir_date}')
    return render(request, 'create_docs/create_docx.html', {'clients': clients,
                                                            'standart': standart,
                                                            'torg12': torg12})