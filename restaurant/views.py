from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.views.generic.list import ListView

from .models import Restaurant

# Create your views here.
def index(request):
    return render(request, "restaurant/list.html")


def restaurant_list(request, list=None):
    sort = request.GET.get("order", "id")
    restaurants = Restaurant.objects.order_by(sort)
    user = User.objects.latest("id")

    if list == "bookmark":
        restaurants = restaurants.filter(users_bookmark=user)
    elif list == "visited":
        restaurants = restaurants.filter(users_visit=user)

    return render(
        request, "restaurant/list.html", {"restaurants": restaurants, "list": list}
    )
