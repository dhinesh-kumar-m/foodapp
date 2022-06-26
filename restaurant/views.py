from audioop import reverse

from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic.list import ListView

from .forms import RatingForm
from .models import Restaurant

# Create your views here.
def index(request):
    return render(request, "restaurant/list.html")


def restaurant_list(request, list=None):
    sort = request.GET.get("order", "id")
    search = request.GET.get("search", None)
    restaurants = Restaurant.objects.order_by(sort)
    user = request.user

    if list == "bookmark":
        restaurants = restaurants.filter(users_bookmark=user)
    elif list == "visited":
        restaurants = restaurants.filter(users_visit=user)

    if search:
        restaurants = restaurants.filter(title__icontains=search)

    return render(
        request, "restaurant/list.html", {"restaurants": restaurants, "list": list}
    )


def restaurant_detail(request, id):
    restaurant = get_object_or_404(Restaurant, id=id)
    return render(request, "restaurant/detail.html", {"restaurant": restaurant})


def add_review(request, id):
    restaurant = get_object_or_404(Restaurant, id=id)
    form = RatingForm(request.POST)
    if form.is_valid():
        review = form.save(commit=False)
        review.restaurant = restaurant
        review.user = request.user
        review.save()
    return redirect(reverse("restaurant:restaurant_detail", args=[id]))
