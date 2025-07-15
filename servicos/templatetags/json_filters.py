from django import template
import json
from decimal import Decimal

register = template.Library()

@register.filter(name='json')
def json_filter(value):
    def decimal_default(obj):
        if isinstance(obj, Decimal):
            return float(obj)
        raise TypeError

    return json.dumps(value, default=decimal_default) 