from django.urls import path

from . import views

app_name = "spotlight"

urlpatterns = [
    path("", views.SpotlightList.as_view(), name="spotlight_list"),
]
