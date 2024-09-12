from django.urls import path, register_converter

from . import views
from .converters import DateConverter


register_converter(DateConverter, 'date')


urlpatterns = [
    path("", views.render_groups, name="render_groups"),
    path("api/<str:group_name>/<date:date>", views.get_table_by_date, name="get_table_by_date"),
    path("api/groups", views.get_all_groups, name="get_all_groups"),
    path("<str:group_name>/today", views.redirect_today, name="redirect_today"),
    path("<str:group_name>/<date:date>", views.render_date, name="render_date"),
]
