

class Rqst:
    """
    Request object helper
    """

    @classmethod
    def get_post_get_param(cls, request, name, default_value):
        """
        Retrieve either POST or GET variable from the request object

        :param request: the request object
        :param name: the name
        :param default_value: the default value if not found
        :return:
        """
        return request.POST.get(name, request.GET.get(name, default_value))

    @classmethod
    def get_pk_or_id(cls, request, pk_keys=('pk', 'id'), default_value=None, cast_int=True):
        """
        Get the primary key or id from the request object.

        :param request: the request object
        :param pk_keys: the key name(s)
        :param default_value:
        :param cast_int: indicate weather to convert the value to integer
        :return: the value of the variable name
        """
        try:
            for k in pk_keys:
                result = cls.get_post_get_param(request, k, None)
                if result is not None:
                    if cast_int:
                        return int(result)
                    return result
        except Exception as ex:
            print('Error: %s' % ex)
        return default_value

    @classmethod
    def is_get_request(cls, request):
        """
        Is the request is GET method.

        :param request: request object
        :return:
        """
        return str(request.method).upper() == 'GET'

    @classmethod
    def is_post_request(cls, request):
        """
        Is the request is GET method.

        :param request: request object
        :return:
        """
        return str(request.method).upper() == 'POST'
