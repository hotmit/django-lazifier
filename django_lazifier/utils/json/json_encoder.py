from datetime import tzinfo
import sys
from decimal import Decimal
from enum import Enum
import uuid
from dateutil import parser
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import QuerySet, Model
from django.db.models.fields.files import FieldFile
from django.utils.functional import Promise
import re
from django_lazifier.utils.builtin_types.datetime import Dt
from django_lazifier.utils.builtin_types.obj import Obj
from django_lazifier.utils.builtin_types.str import Str

try:
    from django.db.models.query import ValuesQuerySet
except Exception as ex:
    ValuesQuerySet = None

try:
    from phonenumber_field.phonenumber import PhoneNumber
except Exception:
    PhoneNumber = None


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
        try:
            if isinstance(o, ValuesQuerySet) or isinstance(o, QuerySet):
                return [x for x in o]
            elif isinstance(o, JsonSerializer):
                return o.get_json_dict()
            elif isinstance(o, Model):
                return Obj.get_dict(o)
            elif isinstance(o, RawJsonString):
                placeholder = '[$RawJson-%s]' % uuid.uuid4()
                self.__raw_json_replacement[placeholder] = o.get_json()
                return placeholder
            elif isinstance(o, tzinfo):
                return str(o)
            elif isinstance(o, Decimal):
                return float(o)
            elif isinstance(o, Enum):
                return o.value
            elif isinstance(o, Promise):
                # translation proxy
                return str(o)
            elif isinstance(o, FieldFile):
                return o.name
            elif isinstance(o, bytes):
                return o.decode('utf-8', 'replace')
            elif PhoneNumber and isinstance(o, PhoneNumber):
                return o.as_national
        except Exception:
            pass
        return str(o)


def _parse_datetime(dct):
    FORMAT_24H = ('%H:%M:%S', '%H:%M')
    FORMAT_12H = ('%I:%M:%S%p', '%I:%M%p', '%I:%M:%S %p', '%I:%M %p', '%I%p', '%I %p')
    def get_time(time_str):
        if Str.contains_any(time_str, 'am', 'pm', 'a.m.', 'p.m.'):
            return Dt.get_time(time_str, FORMAT_12H, default_value=False)
        elif ':' in time_str:
            return Dt.get_time(time_str, FORMAT_24H, default_value=False)
        return False

    def fuzzy_is_datetime(dt):
        # 2014
        year = re.match(r'\d{4}', dt)
        # 10:30pm
        time = re.match(r'\d?\d\d', dt)
        return bool(year or time)

    for k, v in dct.items():
        if isinstance(v, str) and not Str.is_int(v):
            try:
                time_value = get_time(v)
                if time_value is not False:
                    dct[k] = time_value
                elif fuzzy_is_datetime(v):
                    dct[k] = parser.parse(v)
            except:
                pass
    return dct

