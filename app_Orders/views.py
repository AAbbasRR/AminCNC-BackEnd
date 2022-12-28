from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import SubmitOrderSerializer, EditDescriptionOrderSerializer, OrderHistorySerializer
from .models import Orders


class SubmitOrderView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = SubmitOrderSerializer

    def post(self, request, *args, **kwargs):
        ser = self.serializer_class(data=self.request.data, context={"request": request})
        if ser.is_valid(raise_exception=True):
            ser.save()
            return Response({
                'status': True,
                'result': ser.validated_data
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "status": False,
                "message": ser.errors
            }, status=status.HTTP_400_BAD_REQUEST)


class EditDescriptionOrderView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = EditDescriptionOrderSerializer
    lookup_field = "tracking_code"

    def get_queryset(self):
        user = self.request.user
        queryset = Orders.objects.filter(user_and_address__user=user)
        return queryset


class OrderHistoryView(generics.ListAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = OrderHistorySerializer

    def get_queryset(self):
        user = self.request.user
        orders = Orders.objects.filter(user_and_address__user=user)
        return orders
