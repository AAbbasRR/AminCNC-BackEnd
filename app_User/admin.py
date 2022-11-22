from django.contrib import admin
from django.contrib.auth.models import Group

from jalali_date import datetime2jalali
from jalali_date.admin import ModelAdminJalaliMixin

from app_Settings.admin import admin_site

from .models import User, Address

admin.site.unregister(Group)


class UserAddressAdmin(admin.TabularInline):
    model = Address
    extra = 0
    max_num = 0
    can_delete = False
    readonly_fields = (
        'address_description',
        'post_code',
        'receiver',
        'receiver_mobile_number',
    )


class UserAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    inlines = [UserAddressAdmin]
    change_form_template = 'admin/change_form.html'
    fieldsets = [
        ('اطلاعات شخصی کاربر', {
            'fields': (
                (
                    'mobile_number',
                    'is_active'
                ),
                (
                    'first_name',
                    'last_name'
                ),
                (
                    'get_jalali_date_joined',
                    'get_jalali_last_login',
                )
            )
        }),
    ]
    readonly_fields = (
        'mobile_number',
        'is_active',
        'first_name',
        'last_name',
        'get_jalali_date_joined',
        'get_jalali_last_login',
    )
    list_display = (
        'mobile_number',
        'full_name',
        'get_jalali_date_joined',
        'is_active',
        'is_admin'
    )
    search_fields = (
        'mobile_number',
        'full_name',
    )

    def full_name(self, obj):
        return obj.get_full_name()

    full_name.short_description = 'نام و نام خانوادگی'

    def get_jalali_date_joined(self, obj):
        return datetime2jalali(obj.date_joined).strftime('%Y/%m/%d _ %H:%M:%S')

    get_jalali_date_joined.short_description = 'تاریخ ثبت نام'

    def get_jalali_last_login(self, obj):
        return datetime2jalali(obj.last_login).strftime('%Y/%m/%d _ %H:%M:%S')

    get_jalali_last_login.short_description = 'تاریخ آخرین ورود'

    def is_admin(self, obj):
        return obj.is_superuser and obj.is_staff

    is_admin.short_description = 'وضعیت مدیر بودن'
    is_admin.boolean = True

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    class Meta:
        model = User


admin_site.register(User, UserAdmin)
