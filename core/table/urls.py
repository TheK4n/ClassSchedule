from django.urls import path, register_converter

from . import views
from .converters import DateConverter


register_converter(DateConverter, 'date')


urlpatterns = [
    path("", views.render_groups, name="render_groups"),
    path("api/<date:date>/<str:group>", views.get_table_by_date, name="get_table_by_date"),
    path("today/<str:group>/", views.redirect_today, name="redirect_today"),
    path("<date:date>/<str:group>/", views.render_date, name="render_date"),
]
