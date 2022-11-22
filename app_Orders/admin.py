from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe

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
    )


class OrdersAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    inlines = [OrderProductAdmin, ]
    change_form_template = 'admin/change_form.html'
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
                    'delivery_status',
                )
            )
        }),
    ]
    readonly_fields = (
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
    )
    list_display = (
        'user_mobile_number',
        'user_receiver_name',
        'jalali_submit_date',
        'delivery_status',
        'tracking_code',
        'delivery_mode',
    )
    search_fields = (
        'user_and_address__user__mobile_number',
        'user_and_address__receiver',
        'tracking_code',
    )
    ordering = (
        'delivery_status',
        '-submit_date'
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

    class Meta:
        model = Orders


admin_site.register(Orders, OrdersAdmin)
