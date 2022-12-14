from django.apps import AppConfig


class AppUserConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app_User'
    verbose_name = "کاربر"
    verbose_name_plural = "کاربران"

    def ready(self):
        import app_User.signals
