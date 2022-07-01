from django.shortcuts import render
from restaurant.views import RestaurantListFilterMixin

# Create your views here.


class SpotlightList(RestaurantListFilterMixin):
    template_name = "spotlight/list.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(is_spotlighted=True)
        return queryset
