from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe

from jalali_date import datetime2jalali
from jalali_date.admin import ModelAdminJalaliMixin

from app_Settings.admin import admin_site

from .models import PaymentHistory


class PaymentHistoryAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    change_form_template = 'admin/order_change_form.html'
    fieldsets = [
        ('جزيیات پرداخت کننده', {
            'fields': (
                (
                    'client_mobile_number',
                    'order_detail',
                ),
            )
        }),
        ('جزيیات پرداخت', {
            'fields': (
                (
                    'price',
                    'jalali_date',
                    'ref_id',
                ),
            )
        }),
        ('وضعیت پرداخت', {
            'fields': (
                (
                    'status',
                    'portal',
                ),
            )
        }),
    ]
    readonly_fields = (
        'client_mobile_number',
        'order_detail',
        'price',
        'jalali_date',
        'ref_id',
        'status',
        'portal',
    )
    list_display = (
        "ref_id",
        "user_mobile_number",
        "price",
        "jalali_date",
        "portal",
    )
    search_fields = (
        'user__mobile_number',
        'price',
        'ref_id',
    )
    ordering = (
        '-date',
    )

    def user_mobile_number(self, obj):
        return obj.user.mobile_number

    user_mobile_number.short_description = "کاربر پرداخت کننده"

    def jalali_date(self, obj):
        return datetime2jalali(obj.date).strftime('%Y/%m/%d _ %H:%M:%S')

    jalali_date.short_description = 'تاریخ پرداخت'

    def client_mobile_number(self, obj):
        return mark_safe(
            '<a href="{}">{}</a>'.format(
                reverse('admin:app_User_user_change', args=(obj.user.pk,)),
                obj.user.mobile_number
            )
        )

    client_mobile_number.short_description = 'شماره تماس و لینک پروفایل'

    def order_detail(self, obj):
        return mark_safe(
            '<a href="{}">{}</a>'.format(
                reverse('admin:app_Orders_orders_change', args=(obj.order.pk,)),
                obj.order.tracking_code
            )
        )

    order_detail.short_description = 'کد پیگیری سفارش و لینک'

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    class Meta:
        model = PaymentHistory


admin_site.register(PaymentHistory, PaymentHistoryAdmin)
