import re


def snake_case(name):
    """Function to convert CamelCase to snake_case"""
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def camel_case(name):
    words = name.split('_')
    return ''.join((w.capitalize() for w in words))
