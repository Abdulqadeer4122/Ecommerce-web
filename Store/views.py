from django.db.models import Count
from .filter import ProductFilter
from .models import Product, Collection, Reviews, Cart, CartItem, Customer
from rest_framework.response import Response
from .serializer import ProductSerializer, CollectionSerializer, ReviewsSerializer, CartSerializer, CartItemSerializer, \
    CartItemAddSerializer, CartItemUpdateSerializer, CustomerSerializer
from rest_framework import status
from rest_framework.filters import SearchFilter, OrderingFilter
from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, UpdateModelMixin
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from .permissions import IsAdminOrReadOnly, HasViewPermission


class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAdminUser]

    @action(detail=True, methods=['GET'], permission_classes=[HasViewPermission])
    def history(self, request, pk):
        return Response("Okay")

    @action(detail=False, methods=['GET', 'PUT'], permission_classes=[IsAuthenticated])
    def me(self, request):
        (customer, created) = Customer.objects.get_or_create(id=request.user.id)
        if request.method == "GET":
            serializer = CustomerSerializer(customer)
            return Response(serializer.data)
        elif request.method == "PUT":
            serializer = CustomerSerializer(customer, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)


class ProductViews(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    pagination_class = PageNumberPagination
    filterset_class = ProductFilter
    search_fields = ['title', 'collection__title']
    ordering_fields = ['title', 'unit_price']
    permission_classes = [IsAdminOrReadOnly]

    def get_serializer_context(self):
        return {'request': self.request}

    def destroy(self, request, pk):
        product_object = get_object_or_404(Product, pk=pk)
        if product_object.orderItem.count() > 0:
            return Response({"error": "You can not delete this product due to its use in orderItem"},
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product_object.delete()
        return Response(status=status.HTTP_201_CREATED)


class CollectionViews(ModelViewSet):
    queryset = Collection.objects.annotate(product_count=Count('product'))
    serializer_class = CollectionSerializer
    permission_classes = [IsAdminOrReadOnly]

    def destroy(self, request, pk):
        collection_object = get_object_or_404(Collection.objects.annotate(product_count=Count('product')), pk=pk)
        if collection_object.product_count > 0:
            return Response({"error": "You can not delete this Collection due to its use in Products"},
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)
        collection_object.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ReviewsViews(ModelViewSet):
    serializer_class = ReviewsSerializer

    def get_queryset(self):
        # Assuming 'product_pk' is the name of the URL keyword argument for the product's primary key
        product_pk = self.kwargs.get('product_id_pk')
        print(product_pk)
        if product_pk is not None:
            return Reviews.objects.filter(product_id=product_pk)
        return Reviews.objects.none()

    def get_serializer_context(self):
        return {'product_id': self.kwargs.get('product_id_pk')}


class CartViews(CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, GenericViewSet):
    queryset = Cart.objects.prefetch_related('item__product').all()
    serializer_class = CartSerializer


class CartItemViews(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_serializer_class(self):

        if self.request.method == 'POST':
            return CartItemAddSerializer
        elif self.request.method == 'PATCH':
            return CartItemUpdateSerializer
        return CartItemSerializer

    def get_queryset(self):
        cart_id = self.kwargs.get('cart_pk')
        return CartItem.objects.select_related('product').filter(cart_id=cart_id)

    def get_serializer_context(self):
        cart_id = self.kwargs.get('cart_pk')
        return {'cart_id': cart_id}
# class ProductList(APIView):
#     def get(self,request):
#         products = Product.objects.select_related('collection')
#         product_serializer = ProductSerializer(products, many=True)
#         return Response({'data': product_serializer.data})
#     def post(self,request):
#         product_serializer = ProductSerializer(data=request.data)
#         product_serializer.is_valid(raise_exception=True)
#         product_serializer.save()
#         return Response(status=status.HTTP_201_CREATED)

# class ProductDetail(RetrieveUpdateDestroyAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#
#     def delete(self, request, pk):
#         product_object = get_object_or_404(Product, pk=pk)
#         if product_object.orderItem.count() > 0:
#             return Response({"error": "You can not delete this product due to its use in orderItem"},
#                             status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         product_object.delete()
#         return Response(status=status.HTTP_201_CREATED)


# class ProductDetail(APIView):
#     def get(self,request,pk):
#         product_object = get_object_or_404(Product, pk=pk)
#         product_serializer = ProductSerializer(product_object)
#         return Response(product_serializer.data, status=status.HTTP_200_OK)
#     def patch(self,request,pk):
#         product_object = get_object_or_404(Product, pk=pk)
#         product_serializer = ProductSerializer(product_object, data=request.data)
#         product_serializer.is_valid(raise_exception=True)
#         product_serializer.save()
#         return Response(status=status.HTTP_201_CREATED)
#
#     def delete(self,request,pk):
#         product_object = get_object_or_404(Product, pk=pk)
#         product_object.delete()
#         return Response(status=status.HTTP_201_CREATED)


# @api_view(['GET', 'PATCH', 'DELETE'])
# def update_product(request, pk):
#     product_object = get_object_or_404(Product, pk=pk)
#     if request.method == 'GET':
#         product_serializer = ProductSerializer(product_object)
#         return Response(product_serializer.data, status=status.HTTP_200_OK)
#     elif request.method == 'PATCH':
#         product_serializer = ProductSerializer(product_object, data=request.data)
#         product_serializer.is_valid(raise_exception=True)
#         product_serializer.save()
#         return Response(status=status.HTTP_201_CREATED)
#     elif request.method == 'DELETE':
#         product_object.delete()
#         return Response(status=status.HTTP_201_CREATED)


# class CollectionList(ListCreateAPIView):
#     queryset = Collection.objects.annotate(product_count=Count('product'))
#     serializer_class = CollectionSerializer
#
#     def delete(self, request, pk):
#         collection_object = get_object_or_404(Collection.objects.annotate(product_count=Count('product')), pk=pk)
#         if collection_object.product_count > 0:
#             return Response({"error": "You can not delete this Collection due to its use in Products"},
#                             status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         collection_object.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

# @api_view(['GET','POST'])
# def collection_list(request):
#     if request.method=='GET':
#         collections=Collection.objects.annotate(product_count=Count('product')).all()
#         collection_serializer=CollectionSerializer(collections,many=True)
#         print(collections)
#         return Response(collection_serializer.data)
#     elif request.method=='POST':
#         collection_serializer = CollectionSerializer(data=request.data)
#         collection_serializer.is_valid(raise_exception=True)
#         collection_serializer.save()
#         return Response(status=status.HTTP_201_CREATED)


# class CollectionDetail(RetrieveUpdateDestroyAPIView):
#     queryset = Collection.objects.annotate(product_count=Count('product'))
#     serializer_class = CollectionSerializer
#
#     def delete(self, request, pk):
#         collection_object = get_object_or_404(Collection.objects.annotate(product_count=Count('product')), pk=pk)
#         if collection_object.product_count > 0:
#             return Response({"error": "You can not delete this Collection due to its use in Products"},
#                             status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         collection_object.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

# @api_view(['GET', 'PATCH', 'DELETE'])
# def update_or_get(request, pk):
#     collection_object = get_object_or_404(Collection.objects.annotate(product_count=Count('product')), pk=pk)
#     if request.method=='GET':
#         collection_serializer = CollectionSerializer(collection_object)
#         return Response(collection_serializer.data,status=status.HTTP_200_OK)
#     elif request.method=='PATCH':
#         collection_serializer = ProductSerializer(collection_object, data=request.data)
#         collection_serializer.is_valid(raise_exception=True)
#         collection_serializer.save()
#         return Response(status=status.HTTP_201_CREATED)
#     elif request.method=='DELETE':
#         if collection_object.product_count>0:
#             return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         collection_object.delete()
#         return Response(status=status.HTTP_200_OK)
