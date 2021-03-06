
from django import template

register = template.Library()


@register.inclusion_tag('users/templatetags/display_user_location.html')
def display_user_location(user, height):
    return {
        'latitude': user.latitude,
        'longitude': user.longitude,
        'height': height,
    }
