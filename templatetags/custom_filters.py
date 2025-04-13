from django import template

register = template.Library()

@register.filter
def remove_backslashes(value):
    return value.replace('\\', '')

@register.filter
def replace_to_backslashes(value):
    return value.replace('/', '%5c')

@register.filter
def cut(value, arg):
    return value.replace(arg, '')