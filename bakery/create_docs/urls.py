from django.urls import path
from create_docs.views import create_docx

urlpatterns = [
    path('docx/', create_docx, name='create_docx'),
]