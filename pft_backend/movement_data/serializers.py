from rest_framework import serializers
from .models import MovementData

# Serializer to handle budged_data table
class MovDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovementData
        fields = (
            "mov_id",
            "user_id",
            "mov_catg_id",
            "mov_period",
            "mov_value",
            "mov_date",
            "mov_description",
            "period_is_open",
            "record_date",
            "last_update_date"
        )

# Serializer to handle only periods by user
class PeriodUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovementData
        fields = (
            "user_id",
            "mov_period",
            "period_is_open",
            "record_date",
        )

# Serializer to handle updated movements
class MovUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovementData
        fields = (
            "mov_id",
            "mov_catg_id",
            "mov_value",
            "mov_date",
            "mov_description",
            "last_update_date",
        )