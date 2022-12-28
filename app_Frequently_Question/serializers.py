from django.db.models import Min

from rest_framework import exceptions, serializers

from .models import Frequently_Question


class Frequently_QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Frequently_Question
        fields = [
            'question',
            'answer',
        ]
