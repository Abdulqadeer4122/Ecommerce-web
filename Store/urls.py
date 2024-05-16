from django.urls import path, include
from .views import *
from rest_framework_nested import routers
router = routers.SimpleRouter()
router.register('products', ProductViews,basename='products')
router.register('collection', CollectionViews)
router.register('cart',CartViews),
router.register('customer',CustomerViewSet)



cart_router=routers.NestedSimpleRouter(router,r'cart',lookup='cart')
cart_router.register(r'cart-item',CartItemViews,basename='cart-item')


domains_router = routers.NestedSimpleRouter(router, r'products',lookup='product_id')
domains_router.register(r'review', ReviewsViews, basename='review')

urlpatterns = [
    path('', include(router.urls)),
    path('',include(domains_router.urls)),
    path('',include(cart_router.urls))
    # path('product-detail/<int:pk>',ProductDetail.as_view()),
    # path('collections-list/',CollectionList.as_view()),
    # path('collection-detail/<int:pk>/',CollectionDetail.as_view())
]
