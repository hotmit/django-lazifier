from django_lazifier.utils.utils import log_exception


class Byt:

    """
    Src: https://docs.python.org/3/library/functions.html#bytearray
    class bytearray([source[, encoding[, errors]]])

    If it is a string, you must also give the encoding (and optionally, errors) parameters; bytearray() then converts
        the string to bytes using str.encode().
    If it is an integer, the array will have that size and will be initialized with null bytes.
    If it is an object conforming to the buffer interface, a read-only buffer of the object will be used to
        initialize the bytes array.
    If it is an iterable, it must be an iterable of integers in the range 0 <= x < 256, which are used as the initial
        contents of the array.

    """
    @classmethod
    def to_string(cls, byte_array, encoding='uft-8', errors='replace', default_value=None):
        """
        Convert an array of bytes into string.

        :type byte_array: bytes|bytearray
        :param byte_array: the source
        :param encoding: the encoded encoding of the binary
        :param errors: other possible values are 'ignore', 'strict', 'xmlcharrefreplace', 'backslashreplace'
                            and any other name registered via codecs.register_error()
        :param default_value: if can't convert use this value to return
        :rtype: str
        """
        try:
            return byte_array.decode(encoding=encoding, errors=errors)
        except Exception as ex:
            log_exception(ex)
            return default_value

    @classmethod
    def from_string(cls, the_str: str, encoding='uft-8', errors='replace', default_value=None):
        """
        Convert string into bytes

        :param the_str: the string
        :param encoding: encoding of the string
        :param errors: other possible values are 'ignore', 'strict', 'xmlcharrefreplace', 'backslashreplace'
                            and any other name registered via codecs.register_error()
        :param default_value: if can't convert use this value to return
        :return:
        """
        try:
            return the_str.encode(encoding=encoding, errors=errors)
        except Exception as ex:
            log_exception(ex)
            return default_value

    @classmethod
    def from_buffer(cls, buffer):
        """
        Convert buffer to binary data

        :param buffer: buffer
        :rtype: bytearray
        """
        return bytearray(buffer)
