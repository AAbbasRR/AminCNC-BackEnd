from django.contrib import admin

from app_Settings.admin import admin_site

from .models import Newsletter


class NewsletterAdmin(admin.ModelAdmin):
    change_form_template = 'admin/change_form.html'
    list_display = (
        'name',
        'email',
        'created_date',
    )

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    class Meta:
        model = Newsletter


admin_site.register(Newsletter, NewsletterAdmin)
