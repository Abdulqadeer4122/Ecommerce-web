from django.contrib import admin
from django.db.models import Count
from django.utils.html import format_html, urlencode
from django.urls import reverse

from .models import *


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        "slug": ['title']
    }
    autocomplete_fields = ['collection']
    list_display = ('title', 'unit_price', 'inventory_status', 'collection_product')
    list_per_page = 10
    list_select_related = ['collection']

    @admin.display(ordering='inventory')
    def inventory_status(self, Prduct):
        if Prduct.inventory < 50:
            return "Low"
        else:
            return "Okay"

    def collection_product(self, Product):
        return Product.collection.title


# Register your models here.

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "membership", "email", "phone")
    search_fields = ['first_name__istartswith','last_name__istartswith']
    list_editable = ['membership']
    ordering = ['first_name', 'last_name']
    list_per_page = 10


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    autocomplete_fields = ['customer']
    list_display = ["id", 'customer_name', 'placed_at']
    list_per_page = 15
    list_select_related = ['customer']
    ordering = ['id']

    @admin.display(ordering='customer')
    def customer_name(self, Order):
        return (Order.customer.first_name) + " " + (Order.customer.last_name)


@admin.register(Collection)
class CollectionModel(admin.ModelAdmin):
    list_display = ['title', 'product_count']
    search_fields = ['title']

    def product_count(self, Collection):

        url = (reverse('admin:Store_product_changelist') +
               '?' +
               urlencode({
                   'collection_id': Collection.id
               }))
        return format_html('<a href="{}">{}</a>', url, Collection.product_count)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            product_count=Count('product')
        )


admin.site.register(Cart)
admin.site.register(CartItem)

admin.site.register(OrderItem)
