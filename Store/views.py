from django.db.models.functions import Concat
from django.shortcuts import render
from .models import Product, Order, OrderItem, Customer
from django.db.models import Q, F, Count, Func, Value
from  django.db import transaction

# Create your views here.
def get_data(request, order_id):
    total = 0
    queryset = OrderItem.objects.select_related('product').filter(order_id=order_id)
    for q in queryset:
        total += (q.quantity * q.unit_price)
    return render(request, 'index.html', {"query_set": queryset, "total": total})


def get_last_order(request):
    orders = Order.objects.select_related('customer').prefetch_related('order_item__product').order_by('-placed_at')[:5]
    # In these lines i am getting the tottal no of objects wif customer but by adding some new things with that
    # objects = Customer.objects.annotate(full_name=Concat("first_name", Value(' '), "last_name", ))
    # for p in objects:
    #     print(p.full_name)
    customers_with_no_of_orders = Customer.objects.annotate(orders_c=Count('c_order'))
    return render(request, 'orders.html', {'data': orders, "total_order": customers_with_no_of_orders})


























@transaction.atomic()
def practice_query(request, customer_id):
    order=Order()
    order.customer_id=123
    order.payment_status='P'
    order.save()

    order_item=OrderItem()
    order_item.order=order
    order_item.product_id=102
    order_item.quantity=3
    order_item.unit_price=34
    order_item.save()
    return HttpResponse("Hi There ")

