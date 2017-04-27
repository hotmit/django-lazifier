from django.db.models import QuerySet
from django.http import HttpResponse
from django.template import defaultfilters
from django_lazifier.utils.builtin_types.obj import Obj
from django_lazifier.utils.json.json import Json
from django_lazifier.utils.json.json_encoder import RawJsonString


class GeoJson:

    @classmethod
    def get_features(cls, query_set: QuerySet, geometry_field: str, primary_key='pk',
                     filter_list=None, exclude_list=None):
        """
        Convert queryset to a geojson FeatureCollection string.

        :param query_set:   The model QuerySet (ie after filters or .all())
        :param geometry_field:  The field name contains the geometry (point, line, polygon, multipolygon, etc.)
        :param primary_key: The name of the primary key field
        :param filter_list: Which fields to include as the "properties" of the feature.
        :param exclude_list: Which fields to exclude as the "properties" of the feature.
        :return:
        """
        template = '''{ "type": "FeatureCollection",
            "features": [%s]
        }
        '''

        feature_list = []
        sequential_id = 1

        for f in query_set:
            properties = Obj.get_dict(f, filter_list, exclude_list)
            properties.pop(geometry_field, None)
            geometry = Obj.getattr(f, geometry_field)

            feature = dict(type="Feature", geometry=RawJsonString(geometry.geojson), properties=properties)
            feature['id'] = Obj.getattr(f, primary_key, sequential_id)
            feature_json = Json.to_json(feature)
            feature_list.append(feature_json)

            sequential_id += 1

        features = ''
        if feature_list:
            features = ','.join(feature_list)
        return defaultfilters.mark_safe(template % features)

    @classmethod
    def return_features(cls, query_set: QuerySet, geometry_field: str, primary_key='pk',
                        filter_list=None, exclude_list=None):
        """
        Get the features and return the json as HttpResponse.
        See GeoJson.get_features() for documentation

        :param query_set:
        :param geometry_field:
        :param primary_key:
        :param filter_list:
        :param exclude_list:
        :return:
        """

        features = cls.get_features(query_set, geometry_field, primary_key, filter_list, exclude_list)
        return HttpResponse(features, content_type="application/json")
