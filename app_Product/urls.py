from django.urls import path
from .views import *

urlpatterns = [
    path('api/products/index/', ProductIndexView.as_view(), name="index_products"),
    path('api/products/all/', ProductAllView.as_view(), name="all_products"),
    path('api/products/single/<slug:slug>/', SingleProductView.as_view(), name="single_product"),

    path('api/delivery/list/', DeliveryModeListView.as_view(), name="list_deliveries"),
]
