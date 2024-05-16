from django.db.models import Count
from rest_framework import serializers
from .models import Product, Collection, Reviews, Cart, CartItem, Customer
from decimal import Decimal
from core.serializer import UserSerializer


class CustomerSerializer(serializers.ModelSerializer):
    user=UserSerializer()

    class Meta:
        model = Customer
        fields = ['user', 'phone', 'birth_date', 'membership']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'price', 'slug', 'inventory', 'price_with_tax', 'collection']

    price = serializers.DecimalField(max_digits=6, decimal_places=2, source='unit_price')
    price_with_tax = serializers.SerializerMethodField(method_name='calculate_tax')

    def calculate_tax(self, product: Product):
        return round(product.unit_price * Decimal(1.1), 3)


class CollectionSerializer(serializers.ModelSerializer):
    product_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Collection
        fields = ['id', 'title', 'product_count']


class ReviewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reviews
        fields = ['id', 'name', 'desc', 'date', 'product']

    def create(self, validated_data):
        product_id = self.context['product_id']
        return Reviews.objects.create(product_id=product_id, **validated_data)


class ProductAddItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'unit_price']


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductAddItemSerializer()
    total_price = serializers.SerializerMethodField(method_name='calculate_price')

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'total_price']

    def calculate_price(self, cart_item: CartItem):
        return cart_item.product.unit_price * cart_item.quantity


class CartItemAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity']

    def validate_product(self, value):
        if not Product.objects.filter(title=value):
            raise serializers.ValidationError("You enter a wrong product name :")
        else:
            return value

    def save(self, **kwargs):
        print(self.validated_data['product'])
        product = self.validated_data['product']
        quantity = self.validated_data['quantity']
        cart_id = self.context.get('cart_id')

        try:
            cart_item = CartItem.objects.get(cart_id=cart_id, product=product)
            cart_item.quantity += quantity
            cart_item.save()
            self.instance = cart_item
        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(cart_id=cart_id, **self.validated_data)
            self.instance = cart_item
        return self.instance


class CartItemUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['quantity']


class CartSerializer(serializers.ModelSerializer):
    item = CartItemSerializer(many=True, read_only=True)
    id = serializers.UUIDField(read_only=True)
    total_price = serializers.SerializerMethodField(method_name='calculate_t_price')

    class Meta:
        model = Cart
        fields = ['id', 'item', 'total_price']

    def calculate_t_price(self, cart: Cart):
        product_list = [item.quantity * item.product.unit_price for item in cart.item.all()]
        return sum(product_list)
