import json
from jalali_date import datetime2jalali

from rest_framework import serializers, exceptions

from app_Product.models import MaterialModel, Product
from app_User.utils import Redis

from .models import Orders, Delivery_mode, Address, ProductsModel


class AddProductSerializer(serializers.Serializer):
    product_id = serializers.CharField(
        max_length=12,
        required=True,
        allow_blank=False,
        error_messages={
            "required": "ارسال آیدی محصول مادر اجباری است"
        }
    )
    material_id = serializers.IntegerField(
        required=True,
        min_value=1,
        error_messages={
            "required": "ارسال آیدی محصول انتخابی اجباری است"
        }
    )
    number = serializers.IntegerField(
        required=True,
        min_value=1,
        error_messages={
            "required": "ارسال تعداد سفارش از محصول اجباری است"
        }
    )

    def validate(self, attrs):
        find_product = MaterialModel.objects.filter(pk=attrs['material_id']).first()
        if find_product is None or find_product.product.productId != attrs['product_id']:
            raise exceptions.NotFound({
                "product_id": {
                    "data": {
                        "product_id": attrs['product_id'],
                        "material_id": attrs['material_id'],
                    },
                    "message": "محصول سفارش داده شده پیدا نشد"
                },
                "material_id": {
                    "data": {
                        "product_id": attrs['product_id'],
                        "material_id": attrs['material_id'],
                    },
                    "message": "محصول سفارش داده شده پیدا نشد"
                },
            })
        elif find_product.number < attrs['number']:
            raise exceptions.ParseError({
                "number": {
                    "data": {
                        "product_id": attrs['product_id'],
                        "material_id": attrs['material_id'],
                    },
                    "message": "تعداد سفارش شما بیشتر از موجودی میباشد"
                }
            })
        else:
            total_price = float(attrs['number'] * find_product.price)
            reversed_product_discounts = find_product.product.discounts.all().order_by('-number')
            discount_percent = 0
            for discount in reversed_product_discounts:
                if discount.number <= attrs['number']:
                    discount_percent = discount.percent
                    break
            discount_price = total_price * (discount_percent / 100)
            payable_price = total_price - discount_price
            del attrs['product_id']
            del attrs['material_id']
            attrs.update({
                'product_id': find_product.pk,
                'total_price': total_price,
                'payable_price': payable_price,
                'discount_price': discount_price,
            })
            return attrs


class SubmitOrderSerializer(serializers.Serializer):
    products = serializers.ListSerializer(
        child=AddProductSerializer(),
        required=True,
        error_messages={
            "required": "ارسال محصولات سفارش اجباری است"
        }
    )
    user_and_address_id = serializers.IntegerField(
        required=True,
        min_value=1,
        error_messages={
            "required": "ارسال آیدی آدرس برای دریافت سفارش اجباری است"
        }
    )
    delivery_mode_id = serializers.IntegerField(
        required=True,
        min_value=1,
        error_messages={
            "required": "ارسال آیدی نوع ارسال برای دریافت سفارش اجباری است"
        }
    )
    description = serializers.CharField(
        max_length=1000,
        required=False,
        allow_blank=True,
        allow_null=True,
    )

    def validate_user_and_address_id(self, value):
        user = self.context.get("request").user
        address_obj = Address.objects.filter(pk=value).first()
        if address_obj is None or address_obj.user != user:
            return exceptions.NotFound({
                "address_id": "آیدی آدرس ارسال پیدا نشد"
            })
        return value

    def validate_delivery_mode_id(self, value):
        delivery_obj = Delivery_mode.objects.filter(pk=value).first()
        if delivery_obj is None:
            return exceptions.NotFound({
                "delivery_id": "آیدی نوع ارسال پیدا نشد"
            })
        return {
            "id": value,
            "price": delivery_obj.price
        }

    def validate(self, attrs):
        user = self.context.get('request').user
        total_price = 0
        delivery_mode_id = attrs['delivery_mode_id']['id']
        for product in attrs['products']:
            total_price += product['payable_price']
        try:
            total_price += int(attrs['delivery_mode_id']['price'])
        except ValueError:
            pass

        del attrs['delivery_mode_id']
        attrs.update({
            'delivery_mode_id': delivery_mode_id,
            'total_price': total_price,
        })

        redis_management = Redis(user.mobile_number, 'order_cart')
        redis_management.set_value(json.dumps(dict(attrs)))
        redis_management.set_expire(1200)
        return attrs

    def create(self, validated_data):
        products = validated_data.pop("products")
        order_obj = Orders.objects.create(**validated_data)
        for product in products:
            ProductsModel.objects.create(
                order=order_obj,
                product_id=product['product_id'],
                total_price=product['total_price'],
                payable_price=product['payable_price'],
                discount_price=product['discount_price'],
                number=product['number']
            )
        return order_obj


class EditDescriptionOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orders
        fields = (
            'description',
        )


class SingleProductSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField('get_image')

    class Meta:
        model = Product
        fields = (
            'name',
            'slug',
            'image',
        )

    def get_image(self, obj):
        image = obj.product_image.first()
        request = self.context.get("request")
        host = request.get_host()
        protocol = request.build_absolute_uri().split(host)[0]
        protocol = protocol.replace("http", "http") if protocol.split(":")[0] == "http" else protocol
        website_url = protocol + host
        return website_url + image.picture.url


class MaterialSerializer(serializers.ModelSerializer):
    product = SingleProductSerializer(many=False, read_only=True)

    material = serializers.SerializerMethodField('get_material')

    class Meta:
        model = MaterialModel
        fields = [
            'product',
            'material',
        ]

    def get_material(self, obj):
        return f'{obj.material.ingredient} - {obj.material.color} - {obj.size.width}x{obj.size.length}{None if obj.size.height is None else "x" + str(obj.size.height)}'


class UserAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = (
            'address_description',
            'post_code',
        )


class DeliverySerializer(serializers.ModelSerializer):
    class Meta:
        model = Delivery_mode
        fields = (
            'mode_name',
        )


class ProductSerializer(serializers.ModelSerializer):
    product = MaterialSerializer(many=False, read_only=True)

    class Meta:
        model = ProductsModel
        fields = (
            'product',
            'number',
            'total_price',
            'payable_price',
        )


class OrderHistorySerializer(serializers.ModelSerializer):
    user_and_address = UserAddressSerializer(many=False, read_only=True)
    delivery_mode = DeliverySerializer(many=False, read_only=True)

    products = serializers.SerializerMethodField('get_products')
    submit_date = serializers.SerializerMethodField('get_submit_date')

    class Meta:
        model = Orders
        fields = [
            'user_and_address',
            'products',
            'delivery_mode',
            'total_price',
            'submit_date',
            'status',
            'tracking_code',
            'description',
        ]
        read_only_fields = (
            'address',
            'products',
            'delivery_mode',
            'total_price',
            'submit_date',
            'status',
            'tracking_code',
            'description',
        )

    def get_submit_date(self, obj):
        return datetime2jalali(obj.submit_date).strftime('%Y/%m/%d _ %H:%M:%S')

    def get_products(self, obj):
        return ProductSerializer(obj.order_order.all(), many=True, context=self.context).data
