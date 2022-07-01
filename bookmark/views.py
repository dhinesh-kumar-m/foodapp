from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse
from restaurant.models import Restaurant
from restaurant.views import RestaurantListFilterMixin

# Create your views here.


class BookmarkList(LoginRequiredMixin, RestaurantListFilterMixin):
    template_name = "bookmark/list.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(users_bookmark=self.request.user)
        return queryset


def add_bookmark(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    if request.user.restaurants_bookmarked.filter(id=restaurant.id).exists():
        request.user.restaurants_bookmarked.remove(restaurant)
    else:
        request.user.restaurants_bookmarked.add(restaurant)
    return redirect(reverse("restaurant:restaurant_detail", args=[restaurant_id]))
