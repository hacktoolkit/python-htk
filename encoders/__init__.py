# Future Imports
from __future__ import absolute_import

# Python Standard Library Imports
import decimal
import json


class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return "%.2f" % obj
        elif type(obj) == set:
            return list(obj)
        return json.JSONEncoder.default(self, obj)


__all__ = [
    'DecimalEncoder',
]
