from django.urls import path, re_path
from . import views

urlpatterns = [
    # endpoint to get all budget data by user_id
    re_path(f'^all_mov_user/([0-9]+)/?$', views.mov_by_user_api ),
    # endpoint to get all periods open by user_id in descending order
    re_path(f'^all_period_open_user/([0-9]+)/?$', views.get_period_open_user ),
    # endpoint to get and save budget data by user and period
    re_path(f'^mov_user_period/([0-9]+)/([0-9_-]+)/?$', views.mov_by_user_period),
    # endpoint to saving new budget:
    re_path(f'^saving_mov/?$', views.saving_mov),
]