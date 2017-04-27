import sys
from os import path
import json
from django.conf import settings
from django_lazifier.utils.utils import p


class Json:
    @classmethod
    def from_str(cls, s, default_value=None):
        """
        Convert json string into dict
        """
        if s is None:
            return default_value
        s = str(s)

        try:
            return json.loads(s, encoding='utf-8')
        except Exception as ex:
            if settings.DEBUG:
                p('Exception: %s' % ex)
            return default_value

    @classmethod
    def from_file(cls, file_path, relative_root=None, default_value=None):
        """
        Convert a json file to a dict.

        :param relative_root: set this to __file__ to make the path relative
        """
        try:
            if relative_root:
                file_path = path.join(path.dirname(path.abspath(relative_root)), file_path)
            with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
                return json.load(f, encoding='utf-8')
        except Exception as ex:
            if settings.DEBUG:
                p('Exception: %s' % ex)
            return default_value

    @classmethod
    def to_json(cls, obj, pretty=False):
        """
        Convert an object to a json formatted string
        """
        if not obj:
            return '{}'

        try:
            from django_lazifier.utils.json.json_encoder import JsonEncoder
        except ImportError:
            JsonEncoder = sys.modules[__package__ + '.JsonEncoder']

        if not pretty:
            json_str = json.dumps(obj, cls=JsonEncoder, skipkeys=True)
        else:
            json_str = json.dumps(obj, cls=JsonEncoder, skipkeys=True, indent=2)
        return json_str
