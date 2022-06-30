from django.urls import path

from . import views

app_name = "bookmark"

urlpatterns = [
    path("", views.BookmarkList.as_view(), name="bookmark_list"),
    path("<int:restaurant_id>", views.add_bookmark, name="bookmark"),
]
