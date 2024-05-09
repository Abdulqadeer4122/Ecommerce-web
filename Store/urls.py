from django.urls import path, include
from .views import *

urlpatterns = [
    path('<int:order_id>', get_data),
    path('',get_last_order),
    path('practice/<int:customer_id>/',practice_query),

]
