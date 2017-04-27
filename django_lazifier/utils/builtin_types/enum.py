from enum import Enum


class Enm:
    @classmethod
    def from_value(cls, enum_type: Enum, value, default_value=None):
        """
        Get enum entry using the value
        :param enum_type:
        :param value:
        :param default_value:
        :return:
        """
        for e in iter(enum_type):
            if e.value == value:
                return e
        return default_value

    @classmethod
    def from_name(cls, enum_type: Enum, name, default_value=None):
        """
        Get enum entry using the name
        :param enum_type:
        :param name:
        :param default_value:
        :return:
        """
        for e in iter(enum_type):
            if e.name == name:
                return e
        return default_value

    @classmethod
    def is_valid(cls, enum_type: Enum, value):
        """
        Determine if the value specify is a valid enum value
        :param enum_type:
        :param value:
        :return:
        """
        return Enm.from_value(enum_type, value, None) is not None
