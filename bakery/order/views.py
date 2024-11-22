from django.shortcuts import render

from order.models import Drivers, Clients, Products


# Create your views here.

def add_data(request):
    if request.method == 'POST':
        if 'driver' in request.POST and request.POST['driver'] != '':
            Drivers.objects.create(driver=request.POST['driver'])

        if 'client' in request.POST and 'drive' in request.POST and request.POST['client'] != '':
            drive = Drivers.objects.filter(driver=request.POST['drive'])[0]
            Clients.objects.create(client=request.POST['client'], driver_id=drive)

        if 'product' in request.POST and request.POST['product'] != '':
            Products.objects.create(product=request.POST['product'])

    drivers = Drivers.objects.all()
    return render(request, 'order/add_data.html', {'drivers': drivers})