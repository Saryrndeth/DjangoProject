from django import template

register = template.Library()


@register.filter
def times(start, end, step=1):
    return range(start, end, step)


@register.filter
def sub(value, arg):
    return value - arg