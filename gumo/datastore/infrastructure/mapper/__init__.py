import datetime
import typing
import json

from gumo.core.injector import injector
from gumo.datastore.infrastructure.entity_key_mapper import EntityKeyMapper

from google.cloud import datastore


class DatastoreMapperMixin:
    _entity_key_mapper = None
    DatastoreEntity = datastore.Entity

    @property
    def entity_key_mapper(self) -> EntityKeyMapper:
        if self._entity_key_mapper is None:
            self._entity_key_mapper = injector.get(EntityKeyMapper)  # type: EntityKeyMapper

        return self._entity_key_mapper

    def convert_datetime(self, t: datetime.datetime) -> typing.Optional[datetime.datetime]:
        if t is None:
            return

        return datetime.datetime(
            year=t.year,
            month=t.month,
            day=t.day,
            hour=t.hour,
            minute=t.minute,
            second=t.second,
            microsecond=t.microsecond,
            tzinfo=datetime.timezone.utc,
        )

    def loads_json_property(self, b: bytes) -> typing.Union[typing.List, typing.Dict]:
        return json.loads(b.decode('utf-8'))

    def dumps_json_property(self, doc: typing.Dict) -> bytes:
        return json.dumps(doc).encode('utf-8')
