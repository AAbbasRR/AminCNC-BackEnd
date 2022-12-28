from rest_framework import generics, status
from rest_framework.permissions import AllowAny

from .serializers import Frequently_QuestionSerializer
from .paginations import Frequently_QuestionPagination
from .models import Frequently_Question


class Frequently_QuestionIndexView(generics.ListAPIView):
    permission_classes = [AllowAny, ]
    serializer_class = Frequently_QuestionSerializer
    queryset = Frequently_Question.objects.filter(show_in_index=True).order_by('?')[0:6]


class Frequently_QuestionAllView(generics.ListAPIView):
    permission_classes = [AllowAny, ]
    serializer_class = Frequently_QuestionSerializer
    pagination_class = Frequently_QuestionPagination
    queryset = Frequently_Question.objects.all()
