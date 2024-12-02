from django.shortcuts import render
from docxtpl import DocxTemplate
from datetime import datetime, date
import os
from .functions import *
import pandas as pd
from order.models import Orders

# Create your views here.

t = datetime.today()
today = date.today()
now_date = [t.year, t.month, t.day]
day_now = now_date[2] if now_date[2] // 10 > 0 else f'0{now_date[2]}'

def add_xml():
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


def add_docx():
    basedir = 'create_docs/templates/docx/'
    for dir in now_date:
        basedir += f'{dir}/'
        try:
            os.mkdir(f'{basedir}')
        except:
            pass

    for order in Orders.objects.filter(date=t).values('client').distinct():
        doc = DocxTemplate("create_docs/templates/patterns/pattern_standart.docx")

        context = {}
        context['today'] = f'{day_now}.{now_date[1]}.{now_date[0] % 100}'
        client_id = list(order.values())[0]
        create_context_for_docx(client_id, today, context)

        doc.render(context)
        name_doc = f'{context['client']}.docx'
        doc.save(f'{basedir}/{name_doc}')
add_docx()


def create_docx(request):
    return render(request, 'create_docs/create_docx.html')