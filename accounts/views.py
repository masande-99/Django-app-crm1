from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
from accounts.models import *


def home(request):
    orders = Order.objects.all()
    print(orders)
    customers = Customer.objects.all()

    context = {'orders': orders, 'customers': customers}

    return render(request, 'account/dashboard.html', context)


def products(request):
    product = Product.objects.all()
    print(product)

    return render(request, 'account/products.html', {'Products': product})


def customer(request):
    return render(request, 'account/customer.html')
