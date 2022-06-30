from django import template

register = template.Library()


@register.simple_tag
def user_review_exist(request, restaurant):
    return request.user.rating_set.filter(restaurant=restaurant).exists()
