from django.contrib import admin
from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import HttpResponse
from django.urls import path, include, re_path
from django.views.static import serve

from . import settings


static_urlpatterns = [
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
]

urlpatterns = [
    path('', include('schedule.urls')),
    path(f'{settings.ADMIN_URL}/', admin.site.urls),
    path('', include(static_urlpatterns)),
]

if settings.URL_PREFIX:
    urlpatterns = [
        path(f'{settings.URL_PREFIX}/', include(urlpatterns)),
    ]



def pingpong(_: WSGIRequest):
    return HttpResponse("pong")


urlpatterns = [
    path('ping/', pingpong),
    path('', include(urlpatterns)),
]
