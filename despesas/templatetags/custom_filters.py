from django import template

register = template.Library()

@register.filter
def format_currency(value):
    try:
        # Formata o número com 2 casas decimais
        formatted = '{:,.2f}'.format(float(value))
        # Substitui o ponto por X temporariamente (para não confundir com o separador de milhar)
        formatted = formatted.replace('.', 'X')
        # Substitui a vírgula por ponto (separador de milhar)
        formatted = formatted.replace(',', '.')
        # Substitui o X por vírgula (separador decimal)
        formatted = formatted.replace('X', ',')
        return formatted
    except (ValueError, TypeError):
        return value 