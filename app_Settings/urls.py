from django.urls import path
from .views import *

urlpatterns = [
    path('api/all/', OptionView.as_view(), name="option_all"),
]
