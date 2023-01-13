from itertools import product

from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .serializers import ProductSerializer, CategoriesSerializer, SingleProductSerializer, DeliveryModeListSerializer
from .paginations import ProductPagination
from .models import Product, Delivery_mode, Categories


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


class CategoriesAllView(generics.ListAPIView):
    permission_classes = [AllowAny, ]
    serializer_class = CategoriesSerializer
    queryset = Categories.objects.all()


class CategoryProductsView(generics.ListAPIView):
    permission_classes = [AllowAny, ]
    serializer_class = ProductSerializer
    pagination_class = ProductPagination

    def get_queryset(self, *args, **kwargs):
        category_slug = self.kwargs['slug']
        category_obj = Categories.objects.filter(slug=category_slug).first()
        if category_obj is not None:
            products = category_obj.product_categories.all()
            return products
        else:
            Response({
                "status": False,
                "message": "دسته مورد نظر پیدا نشد"
            }, status=status.HTTP_404_NOT_FOUND)


class DeliveryModeListView(generics.ListAPIView):
    permission_classes = [AllowAny, ]
    serializer_class = DeliveryModeListSerializer
    queryset = Delivery_mode.objects.all()
