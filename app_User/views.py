from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .serializers import (
    UserRegisterSerializer,
    UserVerifyRegisterSerializer,
    UserReSendRegisterOTPCodeSerializer,
    UserLoginSerializer,
    CompleteUserDataSerializer,
    ChangePasswordSerializer,
    UserAddressesSerializer
)
from .permissions import CompleteUserProfilePermission, ProfileIsEmptyPermission
from .models import User, Address


class UserRegisterView(generics.CreateAPIView):
    permission_classes = [AllowAny, ]
    serializer_class = UserRegisterSerializer


class UserVerifyRegisterView(generics.GenericAPIView):
    permission_classes = [AllowAny, ]
    serializer_class = UserVerifyRegisterSerializer

    def post(self, request, *args, **kwargs):
        ser = self.serializer_class(data=self.request.data)
        if ser.is_valid(raise_exception=True):
            return Response({
                'status': True,
                'message': 'حساب شما با موفقیت فعال شد'
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "status": False,
                "message": ser.errors[list(ser.errors)[0]][0]
            }, status=status.HTTP_400_BAD_REQUEST)


class UserReSendRegisterOTPCodeView(generics.GenericAPIView):
    permission_classes = [AllowAny, ]
    serializer_class = UserReSendRegisterOTPCodeSerializer

    def post(self, request, *args, **kwargs):
        ser = self.serializer_class(data=self.request.data)
        if ser.is_valid(raise_exception=True):
            return Response({
                'status': True,
                'message': 'کد فعالسازی با موفقیت ارسال شد'
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "status": False,
                "message": ser.errors[list(ser.errors)[0]][0]
            }, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(generics.GenericAPIView):
    permission_classes = [AllowAny, ]
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        ser = self.serializer_class(data=self.request.data)
        if ser.is_valid(raise_exception=True):
            return Response({
                'status': True,
                'result': ser.validated_data
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "status": False,
                "message": ser.errors[list(ser.errors)[0]][0]
            }, status=status.HTTP_400_BAD_REQUEST)


class CompleteUserDataView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated, ProfileIsEmptyPermission]
    serializer_class = CompleteUserDataSerializer

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_object(), data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({
                "status": True,
                "message": "profile updated"
            }, status=status.HTTP_200_OK)


class ChangePasswordView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = ChangePasswordSerializer

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_object(), data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({
                "status": True,
                "message": "password updated"
            }, status=status.HTTP_200_OK)


class UserAddressesListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, CompleteUserProfilePermission]
    serializer_class = UserAddressesSerializer

    def finalize_response(self, request, response, *args, **kwargs):
        response_data = response.data
        response.data = {
            "disable_add_address_permission": Address.objects.filter(user=self.request.user).count() >= 10,
            "data": response_data
        }
        return super(UserAddressesListCreateView, self).finalize_response(request, response, *args, **kwargs)

    def get_queryset(self):
        user = self.request.user
        queryset = Address.objects.filter(user=user)
        return queryset


class UserAddressesEditDeleteView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, CompleteUserProfilePermission]
    serializer_class = UserAddressesSerializer
    lookup_field = 'pk'

    def get_queryset(self):
        user = self.request.user
        queryset = Address.objects.filter(user=user)
        return queryset
