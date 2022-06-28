from django.conf import settings
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator
from django.core.validators import MinValueValidator
from django.db import models
from django.urls import reverse

# Create your models here.

FOOD_TYPE_CHOICES = (
    ("veg", "Veg"),
    ("non-veg", "Non-Veg"),
)


class Cuisine(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Restaurant(models.Model):
    TYPE_CHOICES = (
        ("veg", "Veg"),
        ("vegan", "Vegan"),
        ("non-veg", "Non-Veg"),
    )

    STATUS = (("open", "Open"), ("close", "Close"))

    title = models.CharField(max_length=200)
    cost_for_two = models.DecimalField(max_digits=10, decimal_places=2)
    owner = models.ForeignKey(
        User, related_name="restaurant_owner", on_delete=models.CASCADE
    )
    location = models.CharField(max_length=200, blank=True, null=True)
    address = models.TextField()
    city = models.CharField(max_length=200)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    open_time = models.TimeField()
    close_time = models.TimeField()
    average_rating = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)],
        blank=True,
        null=True,
    )
    status = models.CharField(max_length=10, choices=STATUS, default="open")
    is_spotlighted = models.BooleanField(default=False)
    cuisines = models.ManyToManyField(Cuisine, related_name="restaurants_cuisine")
    users_bookmark = models.ManyToManyField(
        User, related_name="restaurants_bookmarked", blank=True
    )
    users_visit = models.ManyToManyField(
        User, related_name="restaurants_visited", blank=True
    )
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("restaurant:restaurant_detail", args=[self.id])

    def get_image(self):
        if self.restaurant_image.count():
            return self.restaurant_image.order_by("id")[0].image


class Image(models.Model):
    restaurant = models.ForeignKey(
        Restaurant, related_name="restaurant_image", on_delete=models.CASCADE
    )
    image = models.ImageField(upload_to="restaurant/%Y/%m/%d", blank=True)


class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    rating = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)]
    )
    review = models.TextField()


class Menu(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)


class Dish(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    type = models.CharField(max_length=10, choices=FOOD_TYPE_CHOICES)


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to="users/%Y/%m/%d/", blank=True)

    def __str__(self):
        return f"Profile for user {self.user.username}"
