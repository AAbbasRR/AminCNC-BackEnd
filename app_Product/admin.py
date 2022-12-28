from django.contrib import admin

from jalali_date import datetime2jalali
from jalali_date.admin import ModelAdminJalaliMixin

from app_Settings.admin import admin_site

from .models import Discount, Delivery_mode, Product, Picture, MaterialModel, ProductPreparationTime
from .forms import ProductChangeForm


class ProductImageAdmin(admin.TabularInline):
    model = Picture
    extra = 0
    min_num = 1
    max_num = 5


class ProductMaterialAdmin(admin.TabularInline):
    model = MaterialModel
    extra = 0
    min_num = 1


class ProductAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    inlines = [ProductImageAdmin, ProductMaterialAdmin]
    change_form_template = 'admin/change_form.html'
    fieldsets = [
        (None, {
            'fields': (('name', 'slug'), ('show_in_index'))
        }),
        ('توضیحات', {
            'fields': ('short_description', 'description')
        }),
        ('تنظیمات', {
            'fields': ('discounts', 'preparation_time')
        })
    ]
    list_display = (
        'name',
        'slug',
        'get_jalali_created_date',
        'short_description',
        'product_picture',
        'show_in_index'
    )
    search_fields = (
        'name',
        'slug',
        'short_description',
    )
    form = ProductChangeForm

    def get_jalali_created_date(self, obj):
        return datetime2jalali(obj.created_date).strftime('%Y/%m/%d _ %H:%M:%S')

    get_jalali_created_date.short_description = 'تاریخ ایجاد'

    def product_picture(self, obj):
        return obj.product_image.first().get_image_tag()

    product_picture.short_description = 'عکس شاخص'
    product_picture.allow_tags = True

    class Meta:
        model = Product


class DiscountAdmin(admin.ModelAdmin):
    change_form_template = 'admin/change_form.html'
    list_display = (
        'number',
        'percent',
    )
    search_fields = (
        'number',
        'percent',
    )

    class Meta:
        model = Discount


class DeliveryAdmin(admin.ModelAdmin):
    change_form_template = 'admin/change_form.html'
    list_display = (
        'mode_name',
        'price',
    )
    search_fields = (
        'mode_name',
        'price',
    )

    class Meta:
        model = Delivery_mode


admin_site.register(Product, ProductAdmin)
admin_site.register(Discount, DiscountAdmin)
admin_site.register(Delivery_mode, DeliveryAdmin)
admin_site.register(ProductPreparationTime)
