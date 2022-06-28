from django.urls import path

from . import views

app_name = "restaurant"

urlpatterns = [
    path("", views.RestaurantList.as_view(), name="restaurant_list"),
    path("restaurant/bookmark", views.BookmarkList.as_view(), name="bookmark_list"),
    path("restaurant/visited", views.VisitedList.as_view(), name="visited_list"),
    path("restaurant/spotlight", views.SpotlightList.as_view(), name="spotlight_list"),
    path("restaurant/<pk>", views.RestaurantDetail.as_view(), name="restaurant_detail"),
    path("restaurant/review/<pk>", views.AddReview.as_view(), name="review"),
    path(
        "restaurant/review/<pk>/update",
        views.UpdateReview.as_view(),
        name="review_update",
    ),
    path(
        "restaurant/review/<pk>/delete",
        views.DeleteReview.as_view(),
        name="review_delete",
    ),
    path("restaurant/bookmark/<int:id>", views.add_bookmark, name="bookmark"),
    path("restaurant/visited/<int:id>", views.delete_visited, name="remove_visited"),
]
