from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
from .models import *


def home(request):
    return render(request, 'account/dashboard.html')


def products(request):
    product = models.Product.objects.all()
    print(product)

    return render(request, 'account/products.html', {'Products': product})


def customer(request):
    return render(request, 'account/customer.html')
