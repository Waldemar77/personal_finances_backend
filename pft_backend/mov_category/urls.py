from django.urls import path, re_path
from . import views

urlpatterns = [
    # >>> paths for all user data
    re_path(f'^mov_catg/?$', views.mov_category_api),
    re_path(f'^mov_catg/([0-9]+)/?$', views.mov_category_api)
]