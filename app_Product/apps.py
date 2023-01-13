from django.apps import AppConfig


class AppProductConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app_Product'
    verbose_name = "محصول"
    verbose_name_plural = "محصولات"

    def ready(self):
        import app_Product.signals
