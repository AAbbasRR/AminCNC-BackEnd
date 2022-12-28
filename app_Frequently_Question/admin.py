from django.contrib import admin

from app_Settings.admin import admin_site

from .models import Frequently_Question


class Frequently_QuestionAdmin(admin.ModelAdmin):
    change_form_template = 'admin/change_form.html'
    list_display = (
        'question',
        'answer',
        'show_in_index'
    )
    search_fields = (
        'question',
        'answer',
    )

    class Meta:
        model = Frequently_Question


admin_site.register(Frequently_Question, Frequently_QuestionAdmin)
