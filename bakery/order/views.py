from django.shortcuts import render

# Create your views here.

def add_data(request):
    return render(request, 'order/add_data.html')