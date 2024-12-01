from django import forms
from order.models import Products, Clients, Drivers

class ProductForm(forms.ModelForm):
    class Meta:
        model = Products
        fields = '__all__'
        labels = {
            'name': 'Наименование',
            'price': 'Цена',
            'weight': 'Вес'
        }


class ClientsForm(forms.ModelForm):
    class Meta:
        model = Clients
        fields = '__all__'
        labels = {
            'name': 'Покупатель',
            'str_torg12': 'Запись в ТОРГ12',
            'str_standart': 'Стандарт',
            'driver': 'Водитель'
        }


class DriversForm(forms.ModelForm):
    class Meta:
        model = Drivers
        fields = '__all__'
        labels = {
            'name': 'Имя и фамилия'
        }