from django.core.paginator import Paginator
from django.db.models import QuerySet, Manager
from django_lazifier.utils.builtin_types.iter import last_iter
from django_lazifier.utils.builtin_types.obj import Obj
from django_lazifier.utils.json.json import Json


class QrSt:
    @classmethod
    def to_json(cls, qs: QuerySet, related_list: list = None):
        """
        Convert QuerySet to json

        eg. QrSt.to_json(sensor_objects, ['zone', 'facility.name', 'sensor__name']

        :param qs:
        :param related_list: by default no related object is included, this explicitly tell which fields to fetch.
        :return:
        """

        model_list = []
        for m in qs:
            model_dict = Obj.get_dict(m)
            if related_list:
                for rl in related_list:
                    rl = rl.replace('__', '.')
                    attrs = rl.split('.')
                    if attrs:
                        first_attr = attrs.pop(0)
                        cur_obj = Obj.getattr(m, first_attr)
                        cur_dict = Obj.get_dict(cur_obj)
                        model_dict[first_attr] = cur_dict

                        for att, is_last in last_iter(attrs):
                            if cur_obj is None:
                                break

                            nxt = Obj.getattr(cur_obj, att)
                            cur_dict[att] = Obj.get_dict(nxt)
                            cur_obj = nxt

                            if is_last and isinstance(cur_obj, Manager):
                                cur_dict[att] = QrSt.get_list(cur_obj.all())
                            else:
                                cur_dict = cur_dict[att]

            model_list.append(model_dict)

        return Json.to_json(model_list)

    @classmethod
    def get_list(cls, qs: QuerySet):
        """
        Return a list of a dict of each row

        :param qs:
        :return:
        """
        result = []
        for m in qs:
            result.append(Obj.get_dict(m))
        return result

    @classmethod
    def pagination_slice(cls, qs, page_num: int, row_per_page: int):
        """
        Slice the queryset based on the page number.

        :param qs:
        :param page_num:
        :param row_per_page:
        :return:
        """
        paginator = Paginator(qs, row_per_page)
        return paginator.page(page_num)
