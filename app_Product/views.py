from rest_framework import generics, status
from rest_framework.permissions import AllowAny

from .serializers import ProductSerializer, SingleProductSerializer, DeliveryModeListSerializer
from .paginations import ProductPagination
from .models import Product, Delivery_mode


class SingleProductView(generics.RetrieveAPIView):
    permission_classes = [AllowAny, ]
    lookup_field = 'slug'
    serializer_class = SingleProductSerializer
    queryset = Product.objects.all()


class ProductIndexView(generics.ListAPIView):
    permission_classes = [AllowAny, ]
    serializer_class = ProductSerializer
    queryset = Product.objects.filter(show_in_index=True).order_by('?')[0:12]


class ProductAllView(generics.ListAPIView):
    permission_classes = [AllowAny, ]
    serializer_class = ProductSerializer
    pagination_class = ProductPagination
    queryset = Product.objects.all()


class DeliveryModeListView(generics.ListAPIView):
    permission_classes = [AllowAny, ]
    serializer_class = DeliveryModeListSerializer
    queryset = Delivery_mode.objects.all()
