from rest_framework.permissions import BasePermission


class ProfileIsEmptyPermission(BasePermission):
    message = {
        "status": False,
        "message": "حساب شما تکمیل شده است"
    }

    def has_permission(self, request, view):
        if request.user.first_name and request.user.last_name:
            return False
        else:
            return True


class CompleteUserProfilePermission(BasePermission):
    message = {
        "status": False,
        "message": "لطفا اول حساب کاربری خود را تکیمل کنید",
        "need_user_profile": True
    }

    def has_permission(self, request, view):
        if request.method == "GET":
            return True
        if request.user.first_name and request.user.last_name:
            return True
        else:
            return False
