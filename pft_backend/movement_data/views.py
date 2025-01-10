
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from django.db.models import OuterRef, Subquery, Max, IntegerField, ExpressionWrapper
from django.db.models.functions import Cast, Concat, Substr

from .models import MovementData
from .serializers import MovDataSerializer, PeriodUserSerializer, MovUpdateSerializer


@api_view(["GET"])
@csrf_exempt
# API to consult all movement data for user id
def mov_by_user_api(request, id_in=0):
    try:
        if request.method == "GET" and int(id_in) > 0:
            model_mov_data = MovementData.objects.filter(user_id=id_in)
            srlz_mov_data = MovDataSerializer(model_mov_data, many=True)
            return JsonResponse(srlz_mov_data.data, safe=False)
        else:
            return JsonResponse(f"[0] There's an error with your request for id: {id_in}.", safe=False)
    except Exception as e:
        return JsonResponse(f"[-1] Error trying to execute request: {e}", safe=False)

@api_view(["GET"])
@csrf_exempt
# API to consult movement data by user and period.
def mov_by_user_period(request, id_in=0, period=""):
    if request.method == "GET" and int(id_in) > 0 and period != "":
        try:
            model_mov_u_p = (MovementData.objects
                                .filter(user_id=id_in)
                                .filter(mov_period=period))
            srlz_mov_u_p = MovDataSerializer(model_mov_u_p, many=True)
            return JsonResponse(srlz_mov_u_p.data, safe=False)
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
            year_part = Substr('mov_period', 1, 4)
            month_part = Substr('mov_period', 6, 2)

            # Combine year and month parts and cast to integer
            mov_period_numeric = ExpressionWrapper(
                Cast(Concat(year_part, month_part), output_field=IntegerField()),
                output_field=IntegerField()
            )

            # Subquery to get the latest record_date for each budget_period
            latest_period_subquery = MovementData.objects.filter(
                user_id=id_in,
                mov_period=OuterRef('mov_period')
            ).values('mov_period').annotate(
                latest_date=Max('record_date')
            ).values('latest_date')

            # Main query to filter and get distinct mov_periods with the latest record_date
            get_data_distinct = MovementData.objects.filter(
                user_id=id_in,
                record_date=Subquery(latest_period_subquery)
            ).annotate(
                mov_period_numeric=mov_period_numeric
            ).order_by('-mov_period_numeric')

            srlz_period_data = PeriodUserSerializer(get_data_distinct, many=True)
            return JsonResponse(srlz_period_data.data, safe=False)
        else:
            return JsonResponse({"error": f"There's an error with your request for id: {id_in}."}, safe=False)
    except Exception as e:
        return JsonResponse({"error": f"Error trying to execute request: {e}"}, safe=False)

@api_view(["GET"])
@csrf_exempt
# API to consult all periods in movement table by a user id and status opened
def get_period_open_user(request, id_in=0):
    try:
        if request.method == "GET" and int(id_in) > 0:
            # Extract year and month from mov_period
            year_part = Substr('mov_period', 1, 4)
            month_part = Substr('mov_period', 6, 2)

            # Combine year and month parts and cast to integer
            mov_period_numeric = ExpressionWrapper(
                Cast(Concat(year_part, month_part), output_field=IntegerField()),
                output_field=IntegerField()
            )

            # Subquery to get the latest record_date for each budget_period
            latest_period_subquery = MovementData.objects.filter(
                user_id=id_in,
                period_is_open="Y",
                mov_period=OuterRef('mov_period')
            ).values('mov_period').annotate(
                latest_date=Max('record_date')
            ).values('latest_date')

            # Main query to filter and get distinct mov_periods with the latest record_date
            get_data_distinct = MovementData.objects.filter(
                user_id=id_in,
                period_is_open="Y",
                record_date=Subquery(latest_period_subquery)
            ).annotate(
                mov_period_numeric=mov_period_numeric
            ).order_by('-mov_period_numeric')

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
def saving_mov(request):
    # Variables to track behavior:
    count_json_in = 0
    records_saved = 0
    if request.method == "POST":
        try:
            json_mov_given = JSONParser().parse(request)
            count_json_in = len(json_mov_given)

            # serializing each set of records from json file request
            for element in json_mov_given:
                srlz_mov = MovDataSerializer(data=element)
                if srlz_mov.is_valid():
                    srlz_mov.save()
                    records_saved += 1
                else:
                    return JsonResponse(f"[0] There are some errors in your request {srlz_mov}.", safe=False)

            # Checking if count of json request is equal to records saved
            if count_json_in == records_saved:
                return JsonResponse(f"[1] All your records have been saved successfully.", safe=False)
            else:
                return JsonResponse(f"[0] Some of your records haven't been saved.", safe=False)
        except Exception as e:
            return JsonResponse(f"[-1] Error trying to execute request: {e}", safe=False)
    else:
        return JsonResponse(f"[-1] HTTP request is not correct: {request.method}", safe=False)

# Method to update and delete a movement by id_movement
@api_view(['PUT', 'DELETE'])
@csrf_exempt
def update_delete_mov(request, id_mov=0):
    # PUT request to update movements if it's necessary
    if request.method == "PUT" and int(id_mov) > 0:
        try:
            json_update_mov = JSONParser().parse(request)
            mov2update = MovementData.objects.get(pk=id_mov)
            updated_mov_srlz = MovUpdateSerializer(mov2update, data=json_update_mov)
            if updated_mov_srlz.is_valid():
                updated_mov_srlz.save()
                return JsonResponse("[1] Your record has been updated successfully.", safe=False)
            else:
                return JsonResponse(f"[0] There are some errors in your request {updated_mov_srlz}.", safe=False)
        except Exception as e:
            return JsonResponse(f"The movement with id: {id_mov} doesn't exist {e}", safe=False)

    # DELETE request to erase one movement
    elif request.method == "DELETE" and int(id_mov):
        try:
            mov2delete = MovementData.objects.get(pk=id_mov)
            mov2delete.delete()
            return JsonResponse(f"[1] Movement with id {id_mov} has been deleted successfully.", safe=False)
        except Exception as e:
            JsonResponse(f"[0] Movement with id {id_mov} might not exist in our data base. {e}", safe=False)