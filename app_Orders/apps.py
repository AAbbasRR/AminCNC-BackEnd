from django.apps import AppConfig


class AppOrdersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app_Orders'
    verbose_name = "سفارش"
    verbose_name_plural = "سفارشات"

    def ready(self):
        import app_Orders.signals
