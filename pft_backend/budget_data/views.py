
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from django.db.models import OuterRef, Subquery, Max, IntegerField, ExpressionWrapper
from django.db.models.functions import Cast, Concat, Substr

from .models import BudgetData
from .serializers import BudgetDataSerializer, PeriodUserSerializer, ClosePeriodSerializer


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

@api_view(["GET"])
@csrf_exempt
# API to consult all periods created (opened and closed).
def user_all_periods(request, id_in=0):
    try:
        if request.method == "GET" and int(id_in) > 0:
            # Extract year and month from mov_period
            year_part = Substr('budget_period', 1, 4)
            month_part = Substr('budget_period', 6, 2)

            # Combine year and month parts and cast to integer
            budget_period_numeric = ExpressionWrapper(
                Cast(Concat(year_part, month_part), output_field=IntegerField()),
                output_field=IntegerField()
            )

            # Subquery to get the latest record_date for each budget_period
            latest_period_subquery = BudgetData.objects.filter(
                user_id=id_in,
                budget_period=OuterRef('budget_period')
            ).values('budget_period').annotate(
                latest_date=Max('record_date')
            ).values('latest_date')

            # Main query to filter and get distinct mov_periods with the latest record_date
            get_data_distinct = BudgetData.objects.filter(
                user_id=id_in,
                record_date=Subquery(latest_period_subquery)
            ).annotate(
                budget_period_numeric=budget_period_numeric
            ).order_by('-budget_period_numeric')

            srlz_period_data = PeriodUserSerializer(get_data_distinct, many=True)
            return JsonResponse(srlz_period_data.data, safe=False)
        else:
            return JsonResponse({"error": f"There's an error with your request for id: {id_in}."}, safe=False)
    except Exception as e:
        return JsonResponse({"error": f"Error trying to execute request: {e}"}, safe=False)


@api_view(["GET"])
@csrf_exempt
# API to consult all periods budget for a user id and status opened
def get_period_open_user(request, id_in=0):
    try:
        if request.method == "GET" and int(id_in) > 0:
            # Extract year and month from budget_period
            year_part = Substr('budget_period', 1, 4)
            month_part = Substr('budget_period', 6, 2)

            # Combine year and month parts and cast to integer
            budget_period_numeric = ExpressionWrapper(
                Cast(Concat(year_part, month_part), output_field=IntegerField()),
                output_field=IntegerField()
            )

            # Subquery to get the latest record_date for each budget_period
            latest_period_subquery = BudgetData.objects.filter(
                user_id=id_in,
                period_is_open="Si",
                budget_period=OuterRef('budget_period')
            ).values('budget_period').annotate(
                latest_date=Max('record_date')
            ).values('latest_date')

            # Main query to filter and get distinct budget_periods with the latest record_date
            get_data_distinct = BudgetData.objects.filter(
                user_id=id_in,
                period_is_open="Si",
                record_date=Subquery(latest_period_subquery)
            ).annotate(
                budget_period_numeric=budget_period_numeric
            ).order_by('-budget_period_numeric')

            srlz_period_data = PeriodUserSerializer(get_data_distinct, many=True)
            return JsonResponse(srlz_period_data.data, safe=False)
        else:
            return JsonResponse({"error": f"There's an error with your request for id: {id_in}."}, safe=False)
    except Exception as e:
        return JsonResponse({"error": f"Error trying to execute request: {e}"}, safe=False)


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

# Method to update period status (to close period)
@api_view(['PUT'])
@csrf_exempt
def update_close_period(request, id_user, period):
    #period format: yyyy-MM example 2024-12
    try:
        json_update_per = JSONParser().parse(request)

        period_to_update = BudgetData.objects.filter(
            user_id = id_user,
            budget_period = period
        )

        for mov in period_to_update:
            updated_period = ClosePeriodSerializer(mov, data=json_update_per, partial=True)
            if updated_period.is_valid():
                updated_period.save()
                return JsonResponse(f"[1] You have closed the period {period} successfully.", safe=False)
            else:
                return JsonResponse(f"[0] There are some errors in your request {json_update_per}.", safe=False)

    except Exception as e:
        return JsonResponse(f"[0] There are some errors in your request {request}. Check that your user {id_user} or period {period} exist. {e}", safe=False)