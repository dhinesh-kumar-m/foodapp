from django.urls import path

from . import views

app_name = "visited"

urlpatterns = [
    path("", views.VisitedList.as_view(), name="visited_list"),
    path("<int:restaurant_id>", views.delete_visited, name="remove_visited"),
]
