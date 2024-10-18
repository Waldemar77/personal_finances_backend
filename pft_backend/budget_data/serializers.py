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
            "record_date"
        )