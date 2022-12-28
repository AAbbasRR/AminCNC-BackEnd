from django.urls import path
from .views import *

urlpatterns = [
    path('api/register/', UserRegisterView.as_view(), name="register"),
    path('api/register/activate/', UserVerifyRegisterView.as_view(), name="validate_register"),
    path('api/register/resend/', UserReSendRegisterOTPCodeView.as_view(), name="resend_register_code"),
    path('api/login/', UserLoginView.as_view(), name="login"),

    path('api/profile/', CompleteUserDataView.as_view(), name="user_profile"),
    path('api/changepass/', ChangePasswordView.as_view(), name="user_change_pass"),

    path('api/addresses/list_create/', UserAddressesListCreateView.as_view(), name="user_list_create_address"),
    path('api/addresses/edit_delete/<int:pk>/', UserAddressesEditDeleteView.as_view(), name="user_edit_delete_address"),
]
