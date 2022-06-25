from django.shortcuts import get_object_or_404
from django.shortcuts import render

from .models import Restaurant

# Create your views here.
def index(request):
    return render(request, "restaurant/list.html")


def restaurant_list(request):
    restaurants = Restaurant.objects.all()
    return render(request, "restaurant/list.html", {"restaurants": restaurants})
