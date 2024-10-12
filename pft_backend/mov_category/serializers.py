from rest_framework import serializers
from .models import *

# Serializer to work whole table MovCategory
class MovCatgSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovCategory
        fields = (
            "mov_catg_id",
            "main_category",
            "category_name",
            "category_description",
            "record_date",
            "last_update_date",
        )