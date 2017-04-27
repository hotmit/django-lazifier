

class Prm:
    @classmethod
    def get_prefix_kwargs(cls, kwargs: dict, prefix: str, default_param: dict, new_prefix=''):
        """
        Remove param from kwargs and return the extracted result.
        Eg. column_kwargs = Prm.get_prefix_kwargs(kwargs, 'col_', {'size': 10})
            This will remove all the "col_" keywords from kwargs

        :param kwargs:
        :param prefix:
        :param default_param:
        :param new_prefix: replace the old prefix with this one
        :return:
        """
        result = default_param
        prefix_length = len(prefix)
        removed_keys = []

        for k, v in kwargs.items():
            key = str(k)
            if key.startswith(prefix):
                key = new_prefix + key[prefix_length:]
                result[key] = v
                removed_keys.append(k)

        for k in removed_keys:
            kwargs.pop(k, None)

        return result
