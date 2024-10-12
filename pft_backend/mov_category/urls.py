from django.urls import path, re_path
from . import views

urlpatterns = [
    # >>> path for all movement categories
    re_path(f'^all_mov_catg/?$', views.all_mov_category_api),

    # >>> paths for working with id mov_category
    re_path(f'^mov_catg/?$', views.mov_category_api),
    re_path(f'^mov_catg/([0-9]+)/?$', views.mov_category_api)
]