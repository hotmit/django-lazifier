from collections import OrderedDict
from django.db import models, transaction
from django.db.models import Manager, Model
from django_lazifier.utils.builtin_types.iter import index_iter
from django_lazifier.utils.builtin_types.obj import Obj
from django_lazifier.utils.builtin_types.str import Str


class Mdl:
    @classmethod
    def has_field(cls, model: models.Model, field_name: str):
        """
        Check if the model has the column with specified name.
        :param model:
        :param field_name:
        :return:
        """
        for f in model._meta.fields:
            if Str.eq(f.name, field_name):
                return True

        return False

    @classmethod
    def get_field_names(cls, model: models.Model, *args):
        """
        Get the column names for .Values() queryset.
        eg. Employee.values( *Mdl.get_col_names(Employee, 'employer', 'contact') )
        employer and contact are ForeignKey name in Employee model.
        return: [ name, age, position, the_employer__id, the_employer__name, contact__id, contact__* ]

        :param model: The model
        :param args: The field name of the Related Object (do not support many-to-many field)
        :return: [ name, age, position, the_employer__id, the_employer__name, contact__id, contact__* ]
        """
        base_cols = []
        for f in model._meta.fields:
            base_cols.append(f.name)

        result = base_cols

        for field in args:
            if field in base_cols:
                f = model._meta.get_field(field, False)

                if f.rel:
                    related_model = f.rel.to
                    for col in Mdl.get_field_names(related_model):
                        result.append("%s__%s" % (f.name, col))

        return result

    @classmethod
    def get_field_attnames(cls, model: models.Model):
        """
        Get a list of all the attname for the specified model.
        :param model: The model
        :return: list[attname1, attname2]
        """
        return [f.attname for f in model._meta.fields]

    @classmethod
    def get_related_field(cls, model: models.Model, filter_list=None, exclude_list=None, verbose_key=False,
                          related_fields=None):
        if not related_fields:
            return OrderedDict()

        result = OrderedDict.fromkeys(related_fields, None)

        for rf in related_fields:
            rel_field = Obj.getattr(model, rf, None)
            if rel_field:
                if isinstance(rel_field, Manager):
                    values = []
                    for itm in rel_field.all():
                        values.append(Mdl.get_dict(itm, filter_list, exclude_list, verbose_key))
                    result[rf] = values
                else:
                    result[rf] = Obj.get_dict(rel_field)
        return result

    @classmethod
    def get_dict(cls, model: models.Model, filter_list=None, exclude_list=None, verbose_key=False, related_fields=None):
        """
        Extract the values from the instance of the model,
            if the fields is specified then remove other fields not in the list.

        :type related_fields: list|None
        :param model: The model
        :param filter_list:
        :param exclude_list:
        :param verbose_key:
        :param related_fields:
        :return:
        """
        values = Obj.get_dict(model, filter_list=filter_list, exclude_list=exclude_list, verbose_key=verbose_key)
        rel = Mdl.get_related_field(model, filter_list=filter_list, exclude_list=exclude_list, verbose_key=verbose_key,
                                    related_fields=related_fields)
        if rel:
            values.update(rel)

        return values

    @classmethod
    def get_field_verbose(cls, model: Model, field_attnames: list):
        result = OrderedDict()

        for fn in field_attnames:
            try:
                field = model._meta.get_field(fn)

                if hasattr(field, 'verbose_name') and field.verbose_name:
                    result[fn] = field.verbose_name.title
                else:
                    result[fn] = fn
            except Exception:
                # if settings.DEBUG:
                #     p('Exception: %s' % ex)
                result[fn] = fn

        return result

    @classmethod
    def get_display_name(cls, model: Model, field_name, default_value=None):
        field_key = Obj.getattr(model, field_name)
        model_field_names = Mdl.get_field_names(model)
        if field_key is None or field_name not in model_field_names:
            return default_value
        field = model._meta.get_field(field_name)
        choices = Obj.getattr(field, 'choices')

        if choices is None:
            return default_value

        for k, v in choices:
            if k == field_key:
                return v

        return Obj.getattr(model, 'get_%s_display' % field_name, default_value)

    @classmethod
    @transaction.atomic(savepoint=True)
    def bulk_create(cls, model: Model, data: list, field_names: list, default_params: dict=None, manager=None):
        """
        Bulk insert

        :param model: The model
        :param data: list of single field value or list of list of data (eg. [ [1, "hello"], [2, "world"] ]
        :param field_names: list of param name in same order of data (eg. [ 'id', 'favorite' ]
        :param default_params: any default values you want to pass to the model creation (eg. { 'site_id': 10 })
        """

        default_params = default_params or {}
        manager = manager or model._default_manager

        data_list = []
        for d in data:
            row = {}
            row.update(default_params)
            for fn, index0 in index_iter(field_names):
                if not isinstance(d, list):
                    row[fn] = d
                    break
                row[fn] = d[index0]
            data_list.append(model(**row))
        manager.bulk_create(data_list)
