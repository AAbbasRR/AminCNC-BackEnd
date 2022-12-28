from django import forms


class ProductChangeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProductChangeForm, self).__init__(*args, **kwargs)
        self.fields['discounts'].help_text = 'برای انتخاب چند گزینه `ctrl` را نگه دارید و روی گزینه کلیک کنید'
