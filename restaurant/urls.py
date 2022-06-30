from django.urls import path

from . import views

app_name = "restaurant"

urlpatterns = [
    path("", views.RestaurantList.as_view(), name="restaurant_list"),
    path("bookmark", views.BookmarkList.as_view(), name="bookmark_list"),
    path("visited", views.VisitedList.as_view(), name="visited_list"),
    path("spotlight", views.SpotlightList.as_view(), name="spotlight_list"),
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
    path("bookmark/<int:restaurant_id>", views.add_bookmark, name="bookmark"),
    path("visited/<int:restaurant_id>", views.delete_visited, name="remove_visited"),
]
