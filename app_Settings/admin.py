from django.contrib import admin
from django.utils import timezone

from app_Orders.models import Orders

from .models import SiteOptions


class MySettingsAdmin(admin.AdminSite):
    site_title = 'مدیریت'
    site_header = 'پنل ادمین'
    index_title = 'مدیریت سایت'

    def each_context(self, request):
        context = super().each_context(request)
        context.update({
            "order_count": Orders.objects.filter(status="AWC").exclude(submit_date__range=[timezone.now() - timezone.timedelta(hours=1), timezone.now()]).count()
        })
        return context


class SiteOptionsAdmin(admin.ModelAdmin):
    change_form_template = 'admin/change_form.html'
    list_display = (
        'phone_number',
        'address',
        'week_hours_work',
        'weekend_hours_work',
        'low_off_product_inventory'
    )

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False

    class Meta:
        model = SiteOptions


admin_site = MySettingsAdmin()
admin_site.register(SiteOptions, SiteOptionsAdmin)
