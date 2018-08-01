### https://stackoverflow.com/questions/2587119/serialize-the-property-methods-in-a-python-class#2607242

from django.core.serializers.base import Serializer as BaseSerializer
from django.core.serializers.python import Serializer as PythonSerializer
from django.core.serializers.json import Serializer as JsonSerializer

"""
Overriding class to get access to the property car_taken of parkinglot
"""


class ExtBaseSerializer(BaseSerializer):

    def serialize_property(self, obj):
        model = type(obj)
        for field in self.selected_fields:
            if hasattr(model, field) and type(getattr(model, field)) == property:
                self.handle_prop(obj, field)

    def handle_prop(self, obj, field):
        self._current[field] = getattr(obj, field)

    def end_object(self, obj):
        self.serialize_property(obj)

        super(ExtBaseSerializer, self).end_object(obj)


class ExtPythonSerializer(ExtBaseSerializer, PythonSerializer):
    pass


class ExtJsonSerializer(ExtPythonSerializer, JsonSerializer):
    pass