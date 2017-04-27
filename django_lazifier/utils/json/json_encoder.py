import sys
from decimal import Decimal
from enum import Enum
import uuid
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import QuerySet, Model
from django.utils.functional import Promise
from django_lazifier.utils.builtin_types.obj import Obj

try:
    from django.db.models.query import ValuesQuerySet
except Exception as ex:
    ValuesQuerySet = None


class JsonSerializer:
    json_includes = None
    json_excludes = None

    def to_json(self):
        """
        Returns the json string of the current instance of this object.
        """
        try:
            from django_lazifier.utils.json.json import Json
        except ImportError:
            Json = sys.modules[__package__ + '.Json']

        return Json.to_json(self.get_json_dict())

    def get_json_dict(self):
        """
        The dict equivalent of the json object.
        """
        return Obj.get_dict(self, self.json_includes, self.json_excludes)


class RawJsonString:
    """
    Tell json encoder put this string as is to the final json encoding.
    """

    def __init__(self, json_str: str):
        self.json_str = json_str

    def get_json(self):
        return self.json_str


class JsonEncoder(DjangoJSONEncoder):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__raw_json_replacement = {}

    def encode(self, o):
        json_str = super(JsonEncoder, self).encode(o)
        for ph, raw_json in self.__raw_json_replacement.items():
            placeholder = '"%s"' % ph
            json_str = json_str.replace(placeholder, raw_json)
        return json_str

    def default(self, o):
        if isinstance(o, QuerySet) or (ValuesQuerySet is not None and isinstance(o, ValuesQuerySet)):
            return [x for x in o]
        elif isinstance(o, JsonSerializer):
            return o.get_json_dict()
        elif isinstance(o, Model):
            return Obj.get_dict(o)
        elif isinstance(o, RawJsonString):
            placeholder = r'[$RawJson-%s]' % uuid.uuid4()
            self.__raw_json_replacement[placeholder] = o.get_json()
            return placeholder

        elif isinstance(o, Decimal):
            return float(o)
        elif isinstance(o, Enum):
            return o.value
        elif isinstance(o, Promise):
            # translation proxy
            return str(o)

        return super().default(o)
