from django.db.models import Min

from rest_framework import serializers

from .models import Discount, Categories, Product, MaterialModel, Picture, Delivery_mode, ProductPreparationTime


class DiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        fields = [
            'number',
            'percent',
        ]
        read_only_fields = (
            'number',
            'percent',
        )


class ProductPreparationTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductPreparationTime
        fields = '__all__'


class MaterialSerializer(serializers.ModelSerializer):
    material = serializers.SerializerMethodField('get_material')
    size = serializers.SerializerMethodField('get_size')

    class Meta:
        model = MaterialModel
        fields = [
            'id',
            'material',
            'size',
            'price',
            'number',
        ]
        read_only_fields = (
            'material',
            'size',
            'price',
            'number',
        )

    def get_material(self, obj):
        return {
            'color': obj.material.color,
            'ingredient': obj.material.ingredient,
            'description': obj.material.description,
        }

    def get_size(self, obj):
        return {
            'width': int(obj.size.width) if obj.size.width.is_integer() else obj.size.width,
            'length': int(obj.size.length) if obj.size.length.is_integer() else obj.size.length,
            'height': None if obj.size.height is None else int(obj.size.height) if obj.size.height.is_integer() else obj.size.height
        }


class PictureSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField('get_image')

    class Meta:
        model = Picture
        fields = [
            'image'
        ]

    def get_image(self, obj):
        request = self.context.get("request")
        host = request.get_host()
        protocol = request.build_absolute_uri().split(host)[0]
        protocol = protocol.replace("http", "http") if protocol.split(":")[0] == "http" else protocol
        website_url = protocol + host
        return website_url + obj.picture.url


class SingleProductSerializer(serializers.ModelSerializer):
    discounts = DiscountSerializer(many=True, read_only=True)
    preparation_time = ProductPreparationTimeSerializer(many=False, read_only=True)

    images = serializers.SerializerMethodField('get_images')
    materials = serializers.SerializerMethodField('get_materials')

    class Meta:
        model = Product
        fields = [
            'name',
            'productId',
            'slug',
            'short_description',
            'preparation_time',
            'description',
            'materials',
            'discounts',
            'images',
        ]
        read_only_fields = (
            'name',
            'productId',
            'slug',
            'short_description',
            'preparation_time',
            'description',
            'materials',
            'discounts',
            'images'
        )

    def get_images(self, obj):
        return PictureSerializer(obj.product_image.all(), many=True, context=self.context).data

    def get_materials(self, obj):
        return MaterialSerializer(obj.product_product.all(), many=True, context=self.context).data


class ProductSerializer(serializers.ModelSerializer):
    price = serializers.SerializerMethodField("get_price")
    image = serializers.SerializerMethodField("get_image")

    class Meta:
        model = Product
        fields = [
            'name',
            'slug',
            'short_description',
            'price',
            'image'
        ]
        read_only_fields = (
            'name',
            'slug',
            'short_description',
            'price',
            'image'
        )

    def get_price(self, obj):
        return obj.product_product.all().aggregate(Min('price'))['price__min']

    def get_image(self, obj):
        image = obj.product_image.first()
        request = self.context.get("request")
        host = request.get_host()
        protocol = request.build_absolute_uri().split(host)[0]
        protocol = protocol.replace("http", "http") if protocol.split(":")[0] == "http" else protocol
        website_url = protocol + host
        return website_url + image.picture.url


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = (
            'name',
            'slug',
            'location',
        )


class DeliveryModeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Delivery_mode
        fields = [
            "id",
            "mode_name",
            "price",
        ]
