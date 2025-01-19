from django.urls import path, re_path
from . import views

urlpatterns = [
    # endpoint to get all budget data by user_id
    re_path(f'^all_budget_user/([0-9]+)/?$', views.budget_by_user_api ),

    # endpoint to get all periods open by user_id in descending order
    re_path(f'^all_period_user/([0-9]+)/?$', views.user_all_periods ),

    # endpoint to get all periods open by user_id in descending order
    re_path(f'^all_period_open_user/([0-9]+)/?$', views.get_period_open_user ),

    # endpoint to get and save budget data by user and period
    re_path(f'^budget_user_period/([0-9]+)/([0-9_-]+)/?$', views.budget_by_user_period),

    # endpoint to save new budget:
    re_path(f'^saving_budget/?$', views.saving_budget),

    # endpoint to close a budget period:
    re_path(f'^closing_bgt_period/([0-9]+)/([0-9_-]+)/?$', views.update_close_period),
]