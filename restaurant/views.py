from audioop import reverse

from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic.list import ListView

from .filters import RestaurantFilter
from .forms import RatingForm
from .models import Rating
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
    elif list == "spotlighted":
        restaurants = restaurants.filter(is_spotlighted=True)

    if search:
        restaurants = restaurants.filter(title__icontains=search)

    if request.method == "POST":
        restaurants = search_filter(request, restaurants)

    return render(
        request, "restaurant/list.html", {"restaurants": restaurants, "list": list}
    )


class RestaurantList(ListView):
    model = Restaurant
    template_name = "restaurant/list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filter"] = RestaurantFilter(
            self.request.GET, queryset=self.get_queryset()
        )
        return context


class BookmarkList(ListView):
    pass


class VisitedList(ListView):
    pass


class SpotlightList(ListView):
    pass


def search_filter(request, restaurants):
    data = request.POST
    cuisine = data.getlist("cuisine", None)
    rating = data.getlist("rating", None)
    type = data.getlist("types", None)
    status = data.getlist("status", None)

    if cuisine:
        restaurants = restaurants.filter(cuisines__in=cuisine)
    if rating:
        restaurants = restaurants.filter(average_rating__in=rating)
    if type:
        restaurants = restaurants.filter(type__in=type)
    if status:
        restaurants = restaurants.filter(status__in=status)
    return restaurants


def restaurant_detail(request, id):
    restaurant = get_object_or_404(Restaurant, id=id)
    if restaurant not in request.user.restaurants_visited.all():
        restaurant.users_visit.add(request.user)
    user_review = restaurant.rating_set.filter(user=request.user)
    if user_review.count() > 0:
        user_review = user_review[0]
    return render(
        request,
        "restaurant/detail.html",
        {"restaurant": restaurant, "user_review": user_review},
    )


def add_review(request, id):
    restaurant = get_object_or_404(Restaurant, id=id)
    form = RatingForm(request.POST)
    if form.is_valid():
        review = form.save(commit=False)
        review.restaurant = restaurant
        review.user = request.user
        review.save()
    return redirect(reverse("restaurant:restaurant_detail", args=[id]))


def update_review(request, id):
    rating = get_object_or_404(Rating, id=id)
    form = RatingForm(instance=rating, data=request.POST)
    if form.is_valid():
        review = form.save(commit=True)
    return redirect(
        reverse("restaurant:restaurant_detail", args=[rating.restaurant.id])
    )


def delete_review(request, id):
    rating = get_object_or_404(Rating, id=id)
    rating.delete()
    return redirect(
        reverse("restaurant:restaurant_detail", args=[rating.restaurant.id])
    )


def add_bookmark(request, id):
    restaurant = get_object_or_404(Restaurant, id=id)
    if restaurant in request.user.restaurants_bookmarked.all():
        restaurant.users_bookmark.remove(request.user)
    else:
        restaurant.users_bookmark.add(request.user)
    return redirect(reverse("restaurant:restaurant_detail", args=[id]))


def delete_visited(request, id):
    restaurant = get_object_or_404(Restaurant, id=id)
    restaurant.users_visit.remove(request.user)
    return redirect("restaurant:restaurant_list")
