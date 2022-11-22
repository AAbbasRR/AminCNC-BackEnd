from django.contrib import admin

from app_Orders.models import Orders


class MySettingsAdmin(admin.AdminSite):
    site_title = 'مدیریت'
    site_header = 'پنل ادمین'
    index_title = 'مدیریت سایت'

    def each_context(self, request):
        context = super().each_context(request)
        context.update({
            "order_count": Orders.objects.filter(delivery_status=False).count()
        })
        return context


admin_site = MySettingsAdmin()
