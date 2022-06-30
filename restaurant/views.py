from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse
from django.urls import reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.edit import DeleteView
from django.views.generic.edit import UpdateView
from django.views.generic.list import ListView

from .filters import RestaurantFilter
from .forms import RatingForm
from .models import Rating
from .models import Restaurant

# Create your views here.


def redirect_dashboard(request):
    return redirect("restaurant:restaurant_list")


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


class BookmarkList(LoginRequiredMixin, RestaurantListMixin):
    template_name = "restaurant/bookmark/list.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(users_bookmark=self.request.user)
        return queryset


class VisitedList(LoginRequiredMixin, RestaurantListMixin):
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


class RestaurantDetail(LoginRequiredMixin, DetailView):
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


class ReviewMixin:
    model = Rating
    fields = ["rating", "review"]
    template_name = "restaurant/detail.html"

    def get_success_url(self):
        return reverse_lazy(
            "restaurant:restaurant_detail", kwargs={"pk": self.object.restaurant.id}
        )


class AddReview(ReviewMixin, CreateView):
    def form_valid(self, form):
        form = form.save(commit=False)
        form.restaurant = Restaurant.objects.get(pk=self.kwargs["pk"])
        form.user = self.request.user
        form.save()
        return redirect(
            reverse("restaurant:restaurant_detail", args=[self.kwargs["pk"]])
        )


class UpdateReview(ReviewMixin, UpdateView):
    pass


class DeleteReview(ReviewMixin, DeleteView):
    pass


def add_bookmark(request, id):
    restaurant = get_object_or_404(Restaurant, id=id)
    if request.user.restaurants_bookmarked.filter(id=restaurant.id).exists():
        request.user.restaurants_bookmarked.remove(request.user)
    else:
        request.user.restaurants_bookmarked.add(request.user)
    return redirect(reverse("restaurant:restaurant_detail", args=[id]))


def delete_visited(request, id):
    restaurant = get_object_or_404(Restaurant, id=id)
    restaurant.users_visit.remove(request.user)
    return redirect("restaurant:visited_list")
