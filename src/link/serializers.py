from rest_framework import serializers
from rest_framework.serializers import ListSerializer

from link.models import ProtectedResource


class DictListSerializer(ListSerializer):
    def __init__(self, *args, **kwargs):
        super(DictListSerializer, self).__init__(*args, **kwargs)

        meta = getattr(self.child, 'Meta')
        self._group_key = getattr(meta, 'group_key', 'id')
        self._delete_group_key = getattr(meta, 'delete_group_key', False)

    def to_representation(self, data):
        rep = super(DictListSerializer, self).to_representation(data)

        result = {}
        for row in rep:
            key = row.get(self._group_key)

            if self._delete_group_key:
                del row[self._group_key]

            result[key] = row

        return result

    @property
    def data(self):
        return self.to_representation(self.instance)


class ProtectedResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProtectedResource
        fields = ('id', 'password', 'file', 'views_count',)
        read_only_fields = ('id', 'views_count',)
        extra_kwargs = {
            'password': {'write_only': True},
            'file': {'write_only': True},
        }


class PasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=100)


class ReportSerializer(serializers.Serializer):
    date = serializers.DateField(read_only=True)
    visited_links = serializers.IntegerField(read_only=True)
    downloaded_files = serializers.IntegerField(read_only=True)

    class Meta:
        list_serializer_class = DictListSerializer
        group_key = 'date'
        delete_group_key = True
