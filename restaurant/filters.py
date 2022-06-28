import django_filters

from .models import Cuisine
from .models import Restaurant


RATING_CHOICE = (
    ("1", "1"),
    ("2", "2"),
    ("3", "3"),
    ("4", "4"),
    ("5", "5"),
)


class RestaurantFilter(django_filters.FilterSet):

    title = django_filters.CharFilter(field_name="title", lookup_expr="icontains")
    average_rating = django_filters.MultipleChoiceFilter(
        field_name="average_rating", choices=RATING_CHOICE
    )
    cuisines__in = django_filters.filters.ModelMultipleChoiceFilter(
        field_name="cuisines__id",
        to_field_name="id",
        lookup_expr="in",
        queryset=Cuisine.objects.all(),
    )
    type = django_filters.MultipleChoiceFilter(
        field_name="type", choices=Restaurant.TYPE_CHOICES
    )
    status = django_filters.MultipleChoiceFilter(
        field_name="status", choices=Restaurant.STATUS
    )

    order_by = django_filters.OrderingFilter(
        fields=(
            ("average_rating", "average_rating"),
            ("cost_for_two", "cost_for_two"),
        ),
    )

    class Meta:
        model = Restaurant
        fields = ["title", "average_rating", "cuisines", "type", "status", "order_by"]
