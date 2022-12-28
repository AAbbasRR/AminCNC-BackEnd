from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from app_Settings.admin import admin_site

urlpatterns = [
    path('admin/', admin_site.urls, name='admin'),
    path('user/', include('app_User.urls'), name='user'),
    path('options/', include('app_Settings.urls'), name='settings'),
    path('product/', include('app_Product.urls'), name='product'),
    path('order/', include('app_Orders.urls'), name='orders'),
    path('questions/', include('app_Frequently_Question.urls'), name='questions'),
    path('newsletter/', include('app_NewSletter.urls'), name='newsletter'),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()
