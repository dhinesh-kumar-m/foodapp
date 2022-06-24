from django.contrib import admin
from restaurant.models import Dish
from restaurant.models import Menu
from restaurant.models import Restaurant

# Register your models here.


class DishInline(admin.StackedInline):
    model = Dish


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
        return obj.restaurant.name


@admin.register(Restaurant)
class CourseAdmin(admin.ModelAdmin):
    list_display = ["title", "created"]
    list_filter = [
        "created",
    ]
    search_fields = ["title", "overview"]
