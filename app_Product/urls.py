from django.urls import path
from .views import *

urlpatterns = [
    path('api/products/index/', ProductIndexView.as_view(), name="index_products"),
    path('api/products/all/', ProductAllView.as_view(), name="all_products"),
    path('api/products/single/<slug:slug>/', SingleProductView.as_view(), name="single_product"),

    path('api/delivery/list/', DeliveryModeListView.as_view(), name="list_deliveries"),

    path('api/categories/all/', CategoriesAllView.as_view(), name="list_categories"),
    path('api/categories/<slug:slug>/products/', CategoryProductsView.as_view(), name="list_category_products"),
]
