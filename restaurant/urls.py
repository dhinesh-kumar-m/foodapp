from django.urls import path

from . import views

app_name = "restaurant"

urlpatterns = [
    path("", views.RestaurantList.as_view(), name="restaurant_list"),
    path("<pk>", views.RestaurantDetail.as_view(), name="restaurant_detail"),
    path("review/<pk>", views.AddReview.as_view(), name="review"),
    path(
        "review/<pk>/update",
        views.UpdateReview.as_view(),
        name="review_update",
    ),
    path(
        "review/<pk>/delete",
        views.DeleteReview.as_view(),
        name="review_delete",
    ),
]
