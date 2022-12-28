from django.urls import path
from .views import *

urlpatterns = [
    path('api/add/', CreateNewsletterView.as_view()),
]