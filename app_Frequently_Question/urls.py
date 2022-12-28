from django.urls import path
from .views import *

urlpatterns = [
    path('api/index/', Frequently_QuestionIndexView.as_view(), name="index_Frequently_QuestionIndexView"),
    path('api/all/', Frequently_QuestionAllView.as_view(), name="all_Frequently_QuestionIndexView"),
]
