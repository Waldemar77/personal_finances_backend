from django.urls import path, re_path
from . import views

urlpatterns = [
    # endpoint to get all budget data by user_id
    re_path(f'^all_budget_user/([0-9]+)/?$', views.budget_by_user_api ),
    # endpoint to get and save budget data by user and period
    re_path(f'^budget_user_period/([0-9]+)/(\d{4}-\d{2})/?$', views.bugdet_by_user_period)
]