from django.contrib import admin

from app_Settings.admin import admin_site

from .models import Material, Size


class MaterialAdmin(admin.ModelAdmin):
    change_form_template = 'admin/change_form.html'
    list_display = (
        'color',
        'ingredient',
    )
    search_fields = (
        'color',
        'ingredient',
    )

    class Meta:
        model = Material


class SizeAdmin(admin.ModelAdmin):
    change_form_template = 'admin/change_form.html'
    list_display = (
        'width',
        'length',
        'height'
    )
    search_fields = (
        'width',
        'length',
        'height'
    )

    class Meta:
        model = Size


admin_site.register(Material, MaterialAdmin)
admin_site.register(Size, SizeAdmin)
