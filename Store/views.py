from django.shortcuts import render
from .models import Product, Order, OrderItem
from django.db.models import Q, F


# Create your views here.
def get_data(request, order_id):
    total = 0
    queryset = OrderItem.objects.select_related('product').filter(order_id=order_id)
    for q in queryset:
        total += (q.quantity * q.unit_price)
    return render(request, 'index.html', {"query_set": queryset, "total": total})
