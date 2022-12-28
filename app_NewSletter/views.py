from rest_framework import status, generics, views
from rest_framework.permissions import AllowAny

from .serializers import CreateNewsletterSerializer


class CreateNewsletterView(generics.CreateAPIView):
    serializer_class = CreateNewsletterSerializer
    permission_classes = [AllowAny, ]
