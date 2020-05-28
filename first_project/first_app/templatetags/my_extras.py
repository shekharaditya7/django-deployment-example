from django import template

register = template.Library()

def cat(value, arg):
    """
    This cuts out all values of "arg" from the string
    """
    return value.replace(arg,'')


register.filter('cat', cat)
