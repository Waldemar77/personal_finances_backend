from django.urls import path, re_path
from .views import *

urlpatterns = [
    # paths for all user data
    re_path(f'^signup/?$', user_data_api),
    re_path(f'^signup/([0-9]+)/?$', user_data_api),
]