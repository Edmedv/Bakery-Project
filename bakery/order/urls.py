from django.urls import path

from order.views import add_data, print_orders

urlpatterns = [
    path('add_data/', add_data, name='add_data'),
    path('print_orders/', print_orders, name='print_orders'),
]