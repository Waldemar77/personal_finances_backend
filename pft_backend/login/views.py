# from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from django.contrib.auth.hashers import make_password, check_password
import json

from .models import *
from .serializers import *


# >>> function for interacting with all data from userdata table
#@api_view(["GET", "POST", "PUT"])
@csrf_exempt  # >>> this decorator allows to use the request POST, because CSFR is a security level to validate proper request
def user_data_api(request, id_in=0):
    # >>> Figure user data out by id through GET http request
    if request.method == "GET" and int(id_in) > 0:
        # >>> variable to instance a UserData class and filter by id user
        user_model = UserData.objects.filter(user_id=id_in)

        # >>> variable to instance a serializer data for each instance of UserData
        user_srlz = UserSerializer(user_model, many=True)

        return JsonResponse(user_srlz.data)
    elif request.method == "POST":
        # >>> variable to save the Json file from front view
        json_user_data = JSONParser().parse(request)

        # >>> encrypting user password
        psw_encrypted = make_password(json_user_data["user_password"])
        # >>> setting encrypted password into the data from json
        json_user_data["user_password"] = psw_encrypted

        # >>> variable to use UserSerializer
        user_srlz = UserSerializer(json_user_data)

        # >>> validating if the user email exists in the db
        # >>> firstly, validating if the serializer was successful
        if user_srlz.is_valid():
            # >>> variable to save data deserialized
            user_desrlz = user_srlz.validated_data
            # >>> variable to save only the email from json file
            user_email_desrlz = user_desrlz["user_email"]

            # >>> validating if email from db is equals to email deserialized
            user_email_db = UserData.objects.filter(user_email=user_email_desrlz) # >>> return false or true
            if user_email_db:
                return JsonResponse("[2] This email already exists in our DataBase.")
            else:
                user_srlz.save()
                return JsonResponse("[1] Your record has been saved successfully")
        else:
            return JsonResponse(f"[0] There are some errors in your data.{user_srlz.errors}")

