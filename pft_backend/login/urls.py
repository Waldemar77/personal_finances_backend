from django.urls import path, re_path
from . import views

urlpatterns = [
    # paths for all user data
    re_path(f'^signup/?$', views.user_data_api),
    re_path(f'^signup/([0-9]+)/?$', views.user_data_api),
]