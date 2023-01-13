from django.utils.translation import gettext_lazy as _

from rest_framework import serializers, exceptions

from app_Product.models import MaterialModel, Product
from app_History.models import PaymentHistory
from app_User.utils import Redis, Manage_Payment_Portal

from .models import Orders, Delivery_mode, Address, ProductsModel

from jalali_date import datetime2jalali
import json


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
    default_error_messages = {
        "error_when_create_link_payment": _("مشکل در سیستم درگاه پرداخت")
    }

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
            raise exceptions.NotFound({
                "address_id": "آیدی آدرس ارسال پیدا نشد"
            })
        return value

    def validate_delivery_mode_id(self, value):
        delivery_obj = Delivery_mode.objects.filter(pk=value).first()
        if delivery_obj is None:
            raise exceptions.NotFound({
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

        payment_management_obj = Manage_Payment_Portal()
        link = payment_management_obj.create_payment_link(total_price, f"ثبت سفارش کاربر {user.mobile_number} به مبلغ {total_price}")
        if link is None:
            raise exceptions.ParseError(
                self.error_messages['error_when_create_link_payment'], 'error_when_create_link_payment'
            )
        redis_management = Redis(user.mobile_number, f"order_cart_{link['auth_token']}")
        redis_management.set_value(json.dumps(dict(attrs)))
        redis_management.set_expire(1200)

        return link['link']


class CheckPaymentFactorOrderSerializer(serializers.Serializer):
    status = serializers.CharField(
        max_length=3,
        required=True,
        error_messages={
            "required": "ارسال وضعیت پرداخت درگاه پرداخت اجباری است",
        }
    )
    authority = serializers.CharField(
        max_length=40,
        required=True,
        error_messages={
            "required": "ارسال شناسه یکتا درگاه پرداخت اجباری است"
        }
    )

    def __init__(self, *args, **kwargs):
        super(CheckPaymentFactorOrderSerializer, self).__init__(*args, **kwargs)
        self.order_detail = None
        self.user = None
        self.authority = None

    def validate_status(self, value):
        if value.upper() == "OK":
            return value.upper()
        elif value.upper() == "NOK":
            return exceptions.ValidationError("تراکنش ناموفق")
        else:
            return exceptions.ParseError("مقدار ورودی وضعیت، نامعتبر")

    def validate_authority(self, value):
        self.user = self.context.get("request").user
        redis_management = Redis(self.user.mobile_number, f"order_cart_{value}")
        try:
            order_detail = json.loads(redis_management.get_value())
            if order_detail is not None:
                self.order_detail = order_detail
                return value
        except TypeError:
            raise exceptions.ValidationError("پرداخت ناموفق، اتمام زمان ثبت سفارش، لطفا مجددا سعی کنید")

    def validate(self, attrs):
        if self.order_detail is not None:
            payment_management_obj = Manage_Payment_Portal()
            ref_id = payment_management_obj.verify_payment_status(self.order_detail['total_price'], attrs['authority'])
            if ref_id is not None:
                self.authority = attrs['authority']
                return {
                    "order_detail": self.order_detail,
                    "ref_id": str(ref_id)
                }
            else:
                raise exceptions.ValidationError("مشکل در تایید از سمت درگاه پرداخت")
        return True

    def create(self, validated_data):
        order_detail = validated_data['order_detail']
        products = order_detail.pop("products")
        order_obj = Orders.objects.create(**order_detail)
        for product in products:
            ProductsModel.objects.create(
                order=order_obj,
                product_id=product['product_id'],
                total_price=product['total_price'],
                payable_price=product['payable_price'],
                discount_price=product['discount_price'],
                number=product['number']
            )
        PaymentHistory.objects.create(
            user=self.user,
            order=order_obj,
            price=order_detail['total_price'],
            status="SUC",
            ref_id=validated_data['ref_id']
        )
        redis_management = Redis(self.user.mobile_number, f"order_cart_{self.authority}")
        redis_management.delete()
        return {
            "total_price": order_detail['total_price'],
            "ref_id": validated_data['ref_id'],
            "order_tracking_code": order_obj.tracking_code
        }


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
