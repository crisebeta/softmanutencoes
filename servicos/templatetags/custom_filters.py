from django import template

register = template.Library()

@register.filter
def format_currency(value):
    try:
        formatted = '{:,.2f}'.format(float(value))
        formatted = formatted.replace('.', 'X')
        formatted = formatted.replace(',', '.')
        formatted = formatted.replace('X', ',')
        return formatted
    except (ValueError, TypeError):
        return value 