from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils import timezone

from jalali_date import datetime2jalali
from jalali_date.admin import ModelAdminJalaliMixin

from app_Settings.admin import admin_site

from .models import Orders, ProductsModel


class OrderProductAdmin(admin.TabularInline):
    model = ProductsModel
    extra = 0
    max_num = 0
    can_delete = False
    readonly_fields = (
        'product',
        'number',
        'total_price',
        'payable_price',
        'discount_price',
    )


class OrdersAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    inlines = [OrderProductAdmin, ]
    change_form_template = 'admin/order_change_form.html'
    fieldsets = [
        ('جزيیات گیرنده', {
            'fields': (
                (
                    'receiver_name',
                    'receiver_mobile_number',
                    'receiver_address',
                    'receiver_post_code'
                ),
            )
        }),
        ('جزئیات سفارش دهنده', {
            'fields': (
                (
                    'client_mobile_number',
                    'client_full_name',
                ),
            )
        }),
        ('جزئیات سفارش', {
            'fields': (
                (
                    'total_price',
                    'jalali_submit_date',
                    'tracking_code',
                ),
                (
                    'delivery_mode',
                    'description',
                ),
                (
                    'status',
                    'admin_description',
                )
            )
        }),
    ]
    readonly_fields = [
        'receiver_name',
        'receiver_mobile_number',
        'receiver_address',
        'receiver_post_code',
        'client_mobile_number',
        'client_full_name',
        'total_price',
        'jalali_submit_date',
        'tracking_code',
        'delivery_mode',
        'description',
        'status'
    ]
    list_display = (
        'user_mobile_number',
        'user_receiver_name',
        'jalali_submit_date',
        'status',
        'tracking_code',
        'delivery_mode',
    )
    search_fields = (
        'user_and_address__user__mobile_number',
        'user_and_address__receiver',
        'tracking_code',
    )
    ordering = (
        '-submit_date',
    )

    def receiver_name(self, obj):
        return obj.user_and_address.receiver

    receiver_name.short_description = 'نام و نام خانوادگی'

    def receiver_mobile_number(self, obj):
        return obj.user_and_address.receiver_mobile_number

    receiver_mobile_number.short_description = 'شماره تماس'

    def receiver_address(self, obj):
        return obj.user_and_address.address_description

    receiver_address.short_description = 'آدرس'

    def receiver_post_code(self, obj):
        return obj.user_and_address.post_code

    receiver_post_code.short_description = 'کد پستی'

    def client_mobile_number(self, obj):
        return mark_safe(
            '<a href="{}">{}</a>'.format(
                reverse('admin:app_User_user_change', args=(obj.user_and_address.user.pk,)),
                obj.user_and_address.user.mobile_number
            )
        )

    client_mobile_number.short_description = 'شماره تماس و لینک پروفایل'

    def client_full_name(self, obj):
        return obj.user_and_address.user.get_full_name()

    client_full_name.short_description = 'نام و نام خانوادگی'

    def user_mobile_number(self, obj):
        return obj.user_and_address.user.mobile_number

    user_mobile_number.short_description = 'شماره تماس سفارش دهنده'

    def user_receiver_name(self, obj):
        return obj.user_and_address.receiver

    user_receiver_name.short_description = 'نام و نام خانوادگی گیرنده'

    def jalali_submit_date(self, obj):
        return datetime2jalali(obj.submit_date).strftime('%Y/%m/%d _ %H:%M:%S')

    jalali_submit_date.short_description = 'تاریخ ثبت سفارش'

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return True

    def response_change(self, request, obj):
        if "_confirm-order" in request.POST:
            obj.status = "PRE"
            obj.save()
        elif "_success-order" in request.POST:
            obj.status = "SUC"
            obj.save()
        elif "_cancel-order" in request.POST:
            obj.status = "CNS"
            obj.save()
        return super().response_change(request, obj)

    def get_readonly_fields(self, request, obj=None):
        if obj.status != "AWC":
            self.readonly_fields.append("admin_description")
            return self.readonly_fields
        else:
            return self.readonly_fields

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.exclude(submit_date__range=[timezone.now() - timezone.timedelta(hours=1), timezone.now()])
        return queryset

    class Meta:
        model = Orders


admin_site.register(Orders, OrdersAdmin)
