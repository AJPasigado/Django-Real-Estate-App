from django import template
from apps.home.models import HomePage
register = template.Library()


@register.simple_tag
def gethomemodel():
    return HomePage.objects.all()[0]