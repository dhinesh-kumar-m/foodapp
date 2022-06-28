from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from .filters import RestaurantFilter
from .forms import RatingForm
from .models import Rating
from .models import Restaurant

# Create your views here.


class RestaurantListMixin(ListView):
    model = Restaurant

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filter"] = RestaurantFilter(
            self.request.GET, queryset=self.get_queryset()
        )
        return context


class RestaurantList(RestaurantListMixin):
    template_name = "restaurant/list.html"


class BookmarkList(RestaurantListMixin):
    template_name = "restaurant/bookmark/list.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(users_bookmark=self.request.user)
        return queryset


class VisitedList(RestaurantListMixin):
    template_name = "restaurant/visited/list.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(users_visit=self.request.user)
        return queryset


class SpotlightList(RestaurantListMixin):
    template_name = "restaurant/spotlight/list.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(is_spotlighted=True)
        return queryset


class RestaurantDetail(DetailView):
    model = Restaurant
    template_name = "restaurant/detail.html"
    context_object_name = "restaurant"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_review"] = (
            self.get_object().rating_set.filter(user=self.request.user).first()
        )
        return context

    def get_object(self):
        object = super().get_object()
        object.users_visit.add(self.request.user)
        return object


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
