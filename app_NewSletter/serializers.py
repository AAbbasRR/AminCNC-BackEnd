from rest_framework import exceptions, serializers

from .models import Newsletter


class CreateNewsletterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Newsletter
        fields = [
            'name',
            'email',
        ]

    def create(self, validated_data):
        return Newsletter.objects.create(**validated_data)
