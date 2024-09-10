from django.urls import path


from . import views

urlpatterns = [
    path("today/<str:group>", views.today, name="today"),
]
