from rest_framework import generics
from rest_framework.permissions import AllowAny

from .serializers import OptionSerializer
from .models import SiteOptions


class OptionView(generics.ListAPIView):
    permission_classes = [AllowAny, ]
    serializer_class = OptionSerializer
    queryset = SiteOptions.objects.all()
