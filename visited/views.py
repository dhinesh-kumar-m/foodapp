from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from restaurant.views import RestaurantFilterMixin
from restaurant.models import Restaurant
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect

# Create your views here.


class VisitedList(LoginRequiredMixin, RestaurantFilterMixin):
    template_name = "visited/list.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(users_visit=self.request.user)
        return queryset


def delete_visited(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    request.user.restaurants_visited.remove(restaurant)
    return redirect("visited:visited_list")
