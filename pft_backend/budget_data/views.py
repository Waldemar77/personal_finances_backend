from itertools import count
from warnings import catch_warnings
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse

from .models import BudgetData
from .serializers import BudgetDataSerializer

@api_view(["GET"])
@csrf_exempt
# API to consult all budget data for user id
def budget_by_user_api(request, id_in=0):
    try:
        if request.method == "GET" and int(id_in) > 0:
            model_budget_data = BudgetData.objects.filter(user_id=id_in)
            srlz_budget_data = BudgetDataSerializer(model_budget_data, many=True)
            return JsonResponse(srlz_budget_data.data, safe=False)
        else:
            return JsonResponse(f"[0] There's an error with your request for id: {id_in}.", safe=False)
    except Exception as e:
        return JsonResponse(f"[-1] Error trying to execute request: {e}", safe=False)

@api_view(["GET"])
@csrf_exempt
# API to consult budget data by user and period.
def budget_by_user_period(request, id_in=0, period=""):
    if request.method == "GET" and int(id_in) > 0 and period != "":
        try:
            model_budget_u_p = (BudgetData.objects
                                .filter(user_id=id_in)
                                .filter(budget_period=period))
            srlz_budget_u_p = BudgetDataSerializer(model_budget_u_p, many=True)
            return JsonResponse(srlz_budget_u_p.data, safe=False)
        except Exception as e:
            return JsonResponse(f"[-1] Error trying to execute request: {e}", safe=False)
    else:
        return JsonResponse(f"[-1] HTTP request is not correct: {request.method}", safe=False)

@api_view(["POST"])
@csrf_exempt
# API to save budget
# Always we need to receive a list of json records
def saving_budget(request):
    # Variables to track behavior:
    count_json_in = 0
    records_saved = 0
    if request.method == "POST":
        try:
            json_budged_given = JSONParser().parse(request)
            count_json_in = len(json_budged_given)

            # serializing each set of records from json file request
            for element in json_budged_given:
                srlz_budget = BudgetDataSerializer(data=element)
                if srlz_budget.is_valid():
                    srlz_budget.save()
                    records_saved += 1
                else:
                    return JsonResponse(f"[0] There are some errors in your request {srlz_budget}.", safe=False)

            # Checking if count of json request is equal to records saved
            if count_json_in == records_saved:
                return JsonResponse(f"[1] All your records have been saved successfully.", safe=False)
            else:
                return JsonResponse(f"[0] Some of your records haven't been saved.", safe=False)
        except Exception as e:
            return JsonResponse(f"[-1] Error trying to execute request: {e}", safe=False)
    else:
        return JsonResponse(f"[-1] HTTP request is not correct: {request.method}", safe=False)