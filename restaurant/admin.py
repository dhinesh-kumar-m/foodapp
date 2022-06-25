from django.contrib import admin
from restaurant.models import Cuisine
from restaurant.models import Dish
from restaurant.models import Image
from restaurant.models import Menu
from restaurant.models import Restaurant

# Register your models here.


class DishInline(admin.StackedInline):
    model = Dish


class ImageInline(admin.StackedInline):
    model = Image


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = [
        "get_restaurant",
        "name",
    ]
    search_fields = ["get_restaurant", "name"]
    inlines = [DishInline]

    @admin.display(description="Restaurant Name", ordering="restaurant__name")
    def get_restaurant(self, obj):
        return obj.restaurant.title


@admin.register(Restaurant)
class CourseAdmin(admin.ModelAdmin):
    list_display = ["title", "created"]
    list_filter = [
        "created",
    ]
    search_fields = ["title", "overview"]
    inlines = [ImageInline]


@admin.register(Cuisine)
class CourseAdmin(admin.ModelAdmin):
    list_display = ["name"]
    list_filter = [
        "name",
    ]
    search_fields = [
        "name",
    ]
