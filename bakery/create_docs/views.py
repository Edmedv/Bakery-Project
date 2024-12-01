from django.shortcuts import render
from docxtpl import DocxTemplate

# Create your views here.

def add_docx(client):
    from datetime import datetime
    import os

    doc = DocxTemplate("create_docs/templates/patterns/pattern_TORG12.docx")

    context = {'pop': 'Edik'}
    doc.render(context)

    t = datetime.today()
    now_date = [t.year, t.month, t.day]
    basedir = 'create_docs/templates/docx/'
    for dir in now_date:
        basedir += f'{dir}/'
        try:
            os.mkdir(f'{basedir}')
        except:
            pass
    name_doc = f'{client}.docx'
    doc.save(f'{basedir}/{name_doc}')


def create_docx(request):
    add_docx('Документ')
    return render(request, 'create_docs/create_docx.html')