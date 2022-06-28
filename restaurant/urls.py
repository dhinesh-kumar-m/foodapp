from django.urls import path

from . import views

app_name = "restaurant"

urlpatterns = [
    # path("", views.restaurant_list, name="restaurant_list"),
    # path("<slug:list>", views.restaurant_list, name="user_list"),
    path("", views.RestaurantList.as_view(), name="restaurant_list"),
    path("restaurant/bookmark", views.BookmarkList.as_view(), name="bookmark_list"),
    path("restaurant/visited", views.VisitedList.as_view(), name="visited_list"),
    path("restaurant/spotlight", views.SpotlightList.as_view(), name="spotlight_list"),
    path("restaurant/<int:id>", views.restaurant_detail, name="restaurant_detail"),
    path("restaurant/review/<int:id>", views.add_review, name="review"),
    path(
        "restaurant/review/<int:id>/update", views.update_review, name="review_update"
    ),
    path(
        "restaurant/review/<int:id>/delete", views.delete_review, name="review_delete"
    ),
    path("restaurant/bookmark/<int:id>", views.add_bookmark, name="bookmark"),
    path("restaurant/visited/<int:id>", views.delete_visited, name="remove_visited"),
]
