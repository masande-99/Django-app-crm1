from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory


# Create your views here.
from accounts.models import *

from .forms import OrderForm

from .filters import OrderFilter


def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()

    total_customers = customers.count()
    total_orders = orders.count()

    delivered = orders.filter(status="Delivered").count()
    pending = orders.filter(status="Pending").count()

    context = {'orders': orders, 'customers': customers,
               'total_customers': total_customers,
               'total_orders': total_orders, 'delivered': delivered,
               'pending': pending}

    return render(request, 'account/dashboard.html', context)


def products(request):
    product = Product.objects.all()

    return render(request, 'account/products.html', {'Products': product})


def customer(request, pk_test):
    customers = Customer.objects.get(id=pk_test)
    orders = customers.order_set.all()

    order_count = orders.count()

    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs

    context = {'customer':customers, 'orders': orders, 'order_count':order_count, 'myFilter':myFilter}
    return render(request, 'account/customer.html',context)


def createOrder(request, pk):
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('products', 'status'), extra=10)
    customer = Customer.objects.get(id=pk)
    formset = OrderFormSet(queryset=Order.objects.none(), instance=customer)
    # form = OrderForm(initial={'customer': customer})

    if request.method == 'POST':
        # form = OrderForm(request.POST)
        formset = OrderFormSet(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')

    context = {'formset': formset}

    return render(request, 'account/order_form.html', context)


def updateOrder(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {'form': form}

    return render(request, 'account/order_form.html', context)



def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == "POST":
        order.delete()
        return redirect('/')

    context = {'item':order}

    return render(request, 'account/delete.html', context)
