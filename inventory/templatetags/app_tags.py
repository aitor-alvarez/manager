from django import template

register = template.Library()

@register.filter(name='get_status')
def get_status(obj):
    return obj.check_status()