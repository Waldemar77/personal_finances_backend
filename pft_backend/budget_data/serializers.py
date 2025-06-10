from rest_framework import serializers
from .models import BudgetData

# Serializer to handle budged_data table
class BudgetDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = BudgetData
        fields = (
            "budget_id",
            "user_id",
            "mov_catg_id",
            "budget_period",
            "budget_value",
            "budget_description",
            "period_is_open",
            "record_date",
        )

# Serializer to handle only periods by user
class PeriodUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = BudgetData
        fields = (
            "user_id",
            "budget_period",
            "period_is_open",
            "record_date",
        )

# Serializer to close period:
class ClosePeriodSerializer(serializers.Serializer):
    class Meta:
        model = BudgetData
        fields = (
            "period_is_open",
            "close_per_date",
        )

    def update(self, instance, validated_data):
        if "period_is_open" in validated_data and "close_per_date" in validated_data:
            instance.period_is_open = validated_data.get("period_is_open", instance.period_is_open)
            instance.close_per_date = validated_data.get("close_per_date", instance.close_per_date)

        instance.save()
        return instance