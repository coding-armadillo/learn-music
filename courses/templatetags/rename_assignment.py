from django import template

register = template.Library()


@register.filter
def rename_assignment(value):
    return value.lower().replace("assignment", "#")
