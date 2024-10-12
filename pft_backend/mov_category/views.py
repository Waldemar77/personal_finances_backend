from warnings import catch_warnings

from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from django.contrib.auth.hashers import make_password, check_password
import json

from .models import MovCategory
from .serializers import MovCatgSerializer

@api_view(["GET"])
@csrf_exempt
def all_mov_category_api(request):
    # GET request method to consult all categories
    if request.method == "GET":
        try:
            allMovCatg_model = MovCategory.objects.all()

            allMovCatgSrlz = MovCatgSerializer(allMovCatg_model, many=True)

            return JsonResponse(allMovCatgSrlz, safe=False)
        except MovCategory.Error:
            return JsonResponse("[0] There is an error with your request.", safe=False)

@api_view(["GET", "POST", "PUT", "DELETE"])
@csrf_exempt
def mov_category_api(request, enter_id=0):
    # GET request method to consult one category by ID
    if request.method == "GET" and int(enter_id) > 0:
        movCatg_model = MovCategory.objects.filter(mov_catg_id=enter_id)

        movCatgSrlz = MovCatgSerializer(movCatg_model, many=True)

        return JsonResponse(movCatgSrlz, safe=False)

    # POST request method to insert a category
    elif request.method == "POST":
        json_movCatg = JSONParser().parse(request)
        movCatgSrlz = MovCatgSerializer(data=json_movCatg)

        if movCatgSrlz.is_valid():
            movCatgSrlz.save()
            return JsonResponse("[1] Your record has been saved successfully.", safe=False)
        else:
            return JsonResponse(f"[0] There are some errors in your request {movCatgSrlz}.", safe=False)

    # PUT request to update categories if it's necessary
    elif request.method == "PUT" and int(enter_id) > 0:
        json_update_movCatg = JSONParser.parse(request)
        try:
            category2update = MovCategory.objects.get(pk=enter_id)
            updated_movCatgSrlz = MovCatgSerializer(category2update, data=json_update_movCatg)

            if updated_movCatgSrlz.is_valid():
                updated_movCatgSrlz.save()
                return JsonResponse("[1] Your record has been updated successfully.", safe=False)
            else:
                return JsonResponse(f"[0] There are some errors in your request {updated_movCatgSrlz}.", safe=False)
        except MovCategory.DoesNotMatch:
            return JsonResponse(f"The category with id: {enter_id} doesn't exist", safe=False)

    # DELETE request to erase one category
    elif request.method == "DELETE" and int(enter_id):
        try:
            category2delete = MovCategory.objects.get(pk=enter_id)
            category2delete.delete()
            return JsonResponse(f"[1] Category with id {enter_id} has been deleted successfully.", safe=False)
        except MovCategory.DoesNotMath:
            JsonResponse(f"[0] Category with id {enter_id} might not exist in our data base.", safe=False)