from django.urls import path, include
from .views import *

urlpatterns = [
    path('<int:order_id>', get_data)

]
