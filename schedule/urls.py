from django.shortcuts import redirect
from django.urls import path, register_converter

from . import views
from .converters import DateConverter


register_converter(DateConverter, 'date')


urlpatterns = [
    path("groups", views.render_groups, name="render_groups"),
    path("", lambda _: redirect("render_groups")),
    path("api/groups", views.get_all_groups, name="get_all_groups"),
    path("api/groups/<str:group_name>/<date:date>", views.get_schedule_by_date, name="get_schedule_by_date"),
    path("groups/<str:group_name>/today", views.render_today, name="render_today"),
    path("groups/<str:group_name>/<date:date>", views.render_date, name="render_date"),
]
