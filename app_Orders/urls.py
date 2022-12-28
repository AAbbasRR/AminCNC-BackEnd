from django.urls import path
from .views import *

urlpatterns = [
    path('api/submit/', SubmitOrderView.as_view(), name="submit_order"),
    path('api/edit/<str:tracking_code>/', EditDescriptionOrderView.as_view(), name="edit_description_order"),
    path('api/history/', OrderHistoryView.as_view(), name="history_order"),
]
