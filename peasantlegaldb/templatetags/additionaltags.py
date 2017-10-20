from django import template


register = template.Library()

@register.filter
def obj_classname(obj):
    return obj.__class__.__name__

@register.filter
def qs_classname(obj):
    return obj.model.__name__