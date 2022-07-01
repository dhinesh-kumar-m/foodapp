from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse
from django.urls import reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.edit import DeleteView
from django.views.generic.edit import UpdateView
from django.views.generic.list import ListView

from .filters import RestaurantFilter
from .models import Rating
from .models import Restaurant

# Create your views here.


class RestaurantFilterMixin(ListView):
    model = Restaurant

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filter"] = RestaurantFilter(
            self.request.GET, queryset=self.get_queryset()
        )
        return context


class RestaurantList(RestaurantFilterMixin):
    template_name = "restaurant/restaurant/list.html"


class RestaurantDetail(LoginRequiredMixin, DetailView):
    model = Restaurant
    template_name = "restaurant/restaurant/detail.html"
    context_object_name = "restaurant"

    def get_object(self):
        object = super().get_object()
        object.users_visit.add(self.request.user)
        return object


class ReviewMixin:
    model = Rating
    fields = ["rating", "review"]
    template_name = "restaurant/restaurant/detail.html"

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
