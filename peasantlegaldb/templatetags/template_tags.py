from django import template
from django.contrib.auth.models import Group


register = template.Library()

@register.filter
def obj_classname(obj):
    return obj.__class__.__name__


@register.filter
def qs_classname(obj):
    return obj.model.__name__


@register.filter
def field_type(bound_field):
    return bound_field.field.widget__class__.__name__


@register.filter
def input_class(bound_field):
    css_class = ''
    if bound_field.form.is_bound:
        if bound_field.errors:
            css_class = 'is-invalid'
        elif field_type(bound_field) != 'PasswordInput':
            css_class = 'is-valid'
    return 'form-control {}'.format(css_class)


@register.filter
def has_group(user, group_name):

    # first check to see if the group itself exists; if not, return a definite false.
    try:
        group = Group.objects.get(name=group_name)
    except:
        return False

    # return true for superuser.
    if user.is_superuser:
        return True

    # Check to see if the group exists within the user's group_set and return a boolean to the template.
    # Within the template use {% if user | has_group:"<group_name>" %} to check for permissions.
    return user.groups.filter(name=group_name).exists()