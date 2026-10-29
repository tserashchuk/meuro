from django import template

register = template.Library()


@register.filter
def ru_plural(value, forms):
    """forms = «модель,модели,моделей»."""
    try:
        n = abs(int(value))
    except (TypeError, ValueError):
        return ''
    one, few, many = [part.strip() for part in str(forms).split(',')]
    if n % 10 == 1 and n % 100 != 11:
        return one
    if 2 <= n % 10 <= 4 and not (12 <= n % 100 <= 14):
        return few
    return many


@register.filter
def has_blocks(value):
    return isinstance(value, dict) and bool(value.get('blocks'))


@register.filter
def join_attr(queryset, attr):
    parts = []
    for obj in queryset:
        parts.append(str(getattr(obj, attr)))
    return '|'.join(parts)
