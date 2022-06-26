from django.urls import path

from . import views

app_name = "restaurant"

urlpatterns = [
    path("", views.restaurant_list, name="restaurant_list"),
    path("<slug:list>", views.restaurant_list, name="user_list"),
    path("restaurant/<int:id>", views.restaurant_detail, name="restaurant_detail"),
]
