from django.db import models
from uuid import uuid4
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from django.contrib import admin


class Collection(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class Promotion(models.Model):
    description = models.CharField(max_length=255)


# Create your models here.
class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    slug = models.SlugField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    inventory = models.IntegerField()
    last_update = models.DateTimeField(auto_now=True)
    collection = models.ForeignKey(Collection, on_delete=models.PROTECT, related_name='product')

    def __str__(self):
        return self.title


class Reviews(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_review')
    name = models.CharField(max_length=255)
    desc = models.TextField()
    date = models.DateField(auto_now=True)

    def __str__(self):
        return self.desc


class Customer(models.Model):
    MEMBERSHIP_BRONZE = 'B'
    MEMBERSHIP_SILVER = 'S'
    MEMBERSHIP_GOLD = 'G'

    MEMBERSHIP_CHOICES = [
        (MEMBERSHIP_BRONZE, 'Bronze'),
        (MEMBERSHIP_SILVER, 'Silver'),
        (MEMBERSHIP_GOLD, 'Gold')
    ]
    phone = models.CharField(max_length=255)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='customer')
    birth_date = models.DateField(null=True, blank=True)
    membership = models.CharField(max_length=1, choices=MEMBERSHIP_CHOICES, default=MEMBERSHIP_BRONZE)

    @admin.display(ordering='user__first_name')
    def first_name(self):
        return self.user.first_name

    @admin.display(ordering='user__last_name')
    def last_name(self):
        return self.user.last_name

    def email(self):
        return self.user.email

    def __str__(self):
        return "{} {}".format(self.user.first_name, self.user.last_name)

    class Meta:
        permissions = [
            ('cancel_order', 'Can cancel Order'),
            ('view_history','can view history')
        ]


class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE)


class Order(models.Model):
    PENDING = 'P'
    COMPLETE = 'C'
    FAILED = 'F'
    PAYMENT_STATUS_CHOICE = [
        (PENDING, 'Pending'),
        (COMPLETE, 'Complete'),
        (FAILED, 'Failed')
    ]
    placed_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=1, choices=PAYMENT_STATUS_CHOICE, default=PENDING)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name='c_order')

    def __str__(self):
        return self.payment_status


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name='order_item')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='orderItem')
    quantity = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)])
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)


class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    created_at = models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='item')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='item_product')
    quantity = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)])
