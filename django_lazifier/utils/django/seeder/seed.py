from datetime import timedelta
import random
from dateutil.parser import parse
from django.db.models import Model
from django_lazifier.utils.builtin_types.iter import IterBase
from django_lazifier.utils.builtin_types.obj import Obj
from django_lazifier.utils.builtin_types.str import Str


class NumSeed(IterBase):
    def __init__(self, min_inclusive=0, max_non_inclusive=100, output_type=int, decimal_places=0):
        self.min = min_inclusive
        self.max = max_non_inclusive
        self.type = output_type
        self.decimal_places = decimal_places

    def next(self):
        scale = pow(10, self.decimal_places)
        min_num = self.min * scale
        max_num = self.max * scale

        num = random.randrange(min_num, max_num)
        num = self.type(num / (scale * 1.0))
        return num


class DateTimeSeed(IterBase):
    def __init__(self, start, end, linear=False, step_min=1, step_max=5, output_format=None):
        """

        :param start: start datetime (datetime instance or string)
        :param end:  end datetime (datetime instance or string)
        :param linear: date increase upward instead of random order
        :param step_min: value to randomize the increase (in minutes). Only apply to linear == True.
        :param step_max: value to randomize the increase (in minutes). Only apply to linear == True.
        :param output_format: leave this None to get datetime value, else return string
                                (strftime format eg. %Y/%m/%d %H:%M:%S)
        :return:
        """
        self.start = parse(start) if isinstance(start, str) else start
        self.end = parse(end) if isinstance(end, str) else end
        self._current = self.start
        self._diff = (self.end - self.start).total_seconds()

        self.linear = linear
        self.step_min = step_min
        self.step_max = step_max
        self.output_format = output_format

    def _get_delta_step(self):
        if self.step_min == self.step_max:
            return self.step_min
        return random.randrange(self.step_min, self.step_max)

    def _return_value(self, datetime_value):
        if self.output_format is None:
            return datetime_value
        return datetime_value.strftime(self.output_format)

    def next(self):
        if self.linear:
            self._current = self._current + timedelta(minutes=self._get_delta_step())
            return self._return_value(self._current)

        return self._return_value(self.start + timedelta(minutes=random.randrange(1, self._diff)/60))


class DateSeed(DateTimeSeed):
    def _return_value(self, datetime_value):
        result = super()._return_value(datetime_value)
        if isinstance(result, str):
            return result
        return result.date()


class ListSeed(IterBase):
    def __init__(self, *items, random=True):
        """
        :param items: accept list or list of tuple (eg. the choices value)
        """
        if len(items) > 0:
            # for choice tuple
            items = list(items)
            if isinstance(items[0], tuple):
                items = list(dict(items).keys())

        self.items = items or []

        self.random = random
        if not random:
            self.index = 0

    def next(self):
        if self.random:
            return self.items[random.randrange(0, len(self))]
        value = self.items[self.index]
        self.index = self.index + 1
        if self.index >= len(self):
            self.index = 0
        return value


class StringSeed(IterBase):
    def __init__(self, prefix, index=1, postfix=''):
        self.prefix = prefix
        self.index = index
        self.postfix = postfix

    def next(self):
        new_str = '{prefix}{index}{postfix}'.format(prefix=self.prefix, index=self.index, postfix=self.postfix)
        self.index = Str.successor(input=self.index, increment=1, case_sensitive=True, )
        return new_str



class TextSeed(IterBase):
    def __init__(self, min_words=0, max_words=50, paragraph=None):
        ipsum = ('Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aliquam eleifend massa vitae malesuada '
                 'consequat. Phasellus egestas cursus elit, a dapibus nisi mattis ut. Nulla dapibus ac nisi in '
                 'iaculis. Nam urna dui, vehicula imperdiet lacus in, ullamcorper scelerisque elit. Etiam mattis '
                 'condimentum lobortis. Vivamus consectetur tortor metus, ac congue diam venenatis imperdiet. Etiam '
                 'rhoncus pulvinar tortor eget vehicula. Etiam odio felis, tristique ac diam vitae, varius dignissim '
                 'sem. Morbi ut scelerisque sapien, eu sagittis justo. Aliquam lacinia porta condimentum. Nunc '
                 'venenatis, ex non molestie congue, lectus lacus posuere tortor, non pellentesque nisi mauris '
                 'pretium magna. Suspendisse dui nulla, convallis faucibus dolor nec, tincidunt tempor mauris. Aenean '
                 'eu elit risus.')

        paragraph = paragraph or ipsum
        self.word_list = paragraph.split(' ')
        max_words = min(max_words + 1, len(self.word_list))
        self._count_seed = NumSeed(min_words, max_words)

    def next(self):
        return ' '.join(self.word_list[:self._count_seed.next()])


class PostalCodeSeed(IterBase):
    def _num(self):
        return random.randrange(0, 9)

    def _letter(self):
        return chr(random.randrange(65, 91))

    def next(self):
        return '%s%d%s %d%s%d' % (self._letter(), self._num(), self._letter(), self._num(), self._letter(), self._num())


class PhoneSeed(IterBase):
    def next(self):
        return '(%s) %s-%s' % (random.randrange(100, 1000), random.randrange(100, 1000), random.randrange(1000, 10000))


class Seed:
    def __init__(self, model: Model, total_qty=100, batch_size=7000, **model_params):
        self.model = model

        self.data_list = []
        self.qty = total_qty
        self.batch_size = batch_size
        self.model_params = model_params

    def _get_values(self):
        param_values = {}
        for k, v in self.model_params.items():
            if isinstance(v, IterBase):
                param_values[k] = v.next()
            else:
                param_values[k] = v
        return param_values

    def create(self, manager: str = None):
        if not manager:
            manager = 'objects'
        model_manager = Obj.getattr(self.model, manager)

        for i in range(self.qty):
            record = self.model(**self._get_values())
            self.data_list.append(record)
            if len(self.data_list) >= self.batch_size:
                self._bulk_insert(model_manager)
        self._bulk_insert(model_manager)

    def _bulk_insert(self, model_manager):
        if self.data_list:
            batch = {}
            # only use batch_size if it is too big, if the diff is small
            # then we saved one extra query
            if len(self.data_list) - self.batch_size > 100:
                batch = {'batch_size': self.batch_size}
            model_manager.bulk_create(self.data_list, **batch)
            self.data_list = []
