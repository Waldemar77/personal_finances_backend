from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from django.contrib.auth.hashers import make_password, check_password
import json

from .models import UserData
from .serializers import *


# >>> function for interacting with all data from userdata table
@api_view(["GET", "POST", "PUT", "DELETE"])
@csrf_exempt  # >>> this decorator allows to use the request POST, because CSFR is a security level to validate proper request
def user_data_api(request, id_in=0):
    # >>> Figure user data out by id through GET http request
    if request.method == "GET" and int(id_in) > 0:
        # >>> variable to instance a UserData class and filter by id user
        user_model = UserData.objects.filter(user_id=id_in)

        # >>> variable to instance a serializer data for each instance of UserData
        user_srlz = UserSerializer(user_model, many=True)

        return JsonResponse(user_srlz.data, safe=False)

    # >>> POST method to insert a new user data
    elif request.method == "POST":
        # >>> variable to save the Json file from front view
        json_user_data = JSONParser().parse(request)
        #print(f">>> json_user_data {json_user_data}")

        # >>> encrypting user password
        psw_encrypted = make_password(json_user_data["user_password"])
        #print(f">>> psw_encrypted {psw_encrypted}")
        # >>> setting encrypted password into the data from json
        json_user_data["user_password"] = psw_encrypted
        #print(f">>> json_user_data2 {json_user_data}")

        # >>> variable to use UserSerializer
        user_srlz = UserSerializer(data=json_user_data)
        #print(f">>> user_srlz {user_srlz}")

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
                return JsonResponse("[2] This email already exists in our DataBase.", safe=False)
            else:
                user_srlz.save()
                return JsonResponse("[1] Your record has been saved successfully", safe=False)
        else:
            return JsonResponse(f"[0] There are some errors in your data.{user_srlz.errors}", safe=False)

    # >>> PUT method to update user data by id
    elif request.method == "PUT" and int(id_in) > 0:

        # >>> validating if id_user informed by JSON input file exists
        json_user_to_update = JSONParser().parse(request)
        try:
            # >>> consulting and get user to update from UserData model
            user_to_update = UserData.objects.get(pk=id_in)

            # >>> using UserSerializerUpdate to update user got through filter by pk and setting with the user from json
            user_to_update_srlz = UserSerializerUpdate(user_to_update, data=json_user_to_update)

            # >>> if the serializer was validated, it'll save updates
            if user_to_update_srlz.is_valid():
                user_to_update_srlz.save()
                return JsonResponse("[1] Your record has been updated successfully", safe=False)
            else:
                return JsonResponse(f"[0] There are some errors in your data.{user_to_update_srlz.errors}", safe=False)
        except Exception as e:
            return JsonResponse(f"[0] User with id {id_in} might not exist in our data base.{user_to_update_srlz.errors}. {e}", safe=False)

    # >>> DELETE method to delete user by id
    elif request.method == "DELETE" and int(id_in) > 0:
        try:
            user_to_delete = UserData.objects.get(pk=id_in)
            user_to_delete.delete()
            return JsonResponse(f"[1] User with id {id_in} has been deleted successfully.", safe=False)
        except Exception as e:
            return JsonResponse(f"[0] User with id {id_in} might not exist in our data base. {e}", safe=False)

# >>> function to interact only with login user data
@api_view(["POST"])
@csrf_exempt
def login_api(request):
    try:
        # >>> Receipting JSON file from POST request and saving email receipted
        json_user_login = JSONParser().parse(request)
        json_email = json_user_login["user_email"]
        json_pswd = json_user_login["user_password"]

        # >>> Figuring user email out into our database through UserData model
        user_filtered = UserData.objects.filter(user_email=json_email)
        user_pswd = user_filtered[0].user_password

        # >>> using check_password method from django restframework
        is_val_pswd = check_password(json_pswd, user_pswd)

        # >>> if password was found, let's create Json response with user_email and user_id
        if is_val_pswd:
            response_array = {"user_id": user_filtered[0].user_id, "user_email": user_filtered[0].user_email}
            return JsonResponse(response_array, safe=False)
        else:
            return JsonResponse("[0] Email or password does not valid.", safe=False)
    except Exception as e:
        return JsonResponse(f"[0] We cannot find your email. Check your information and try again. {e}", safe=False)