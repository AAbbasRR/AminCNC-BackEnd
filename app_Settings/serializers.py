from rest_framework import serializers

from .models import SiteOptions


class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteOptions
        fields = [
            "id",
            "phone_number",
            "address",
            "week_hours_work",
            "weekend_hours_work",
        ]
