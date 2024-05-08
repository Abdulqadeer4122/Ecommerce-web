from django.shortcuts import render
from .models import Product
from django.db.models import Q, F
from django.http import HttpResponse


# Create your views here.
def get_data(request):
    queryset = Product.objects.values('id', 'title', 'unit_price', 'collection_id__title')
    return render(request, 'index.html', {"products": queryset})
