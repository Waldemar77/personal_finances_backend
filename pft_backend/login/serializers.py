from rest_framework import serializers
from .models import *

# Serializers are created to realize the interaction between main db format to python structure data


# All data from table userdata
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserData
        fields = (
            "user_id",
            "user_email",
            "user_password",
            "user_name",
            "user_last_name",
            "user_occupation_name",
            "user_location_name",
            "signup_date",
            "record_date",
            "last_update_date",
        )


# Only login data from table userdata
class UserSerializerLoginData(serializers.ModelSerializer):
    class Meta:
        model = UserData
        fields = (
            "user_id",
            "user_email",
            "user_password",
        )


# Only data to record updates from table userdata
class UserSerializerUpdate(serializers.ModelSerializer):
    class Meta:
        model = UserData
        fields = (
            "user_password",
            "user_name",
            "user_last_name",
            "user_occupation_name",
            "user_location_name",
            "last_update_date",
        )
