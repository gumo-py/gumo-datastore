import dataclasses

from google.cloud import datastore

from gumo.core import EntityKey

from gumo.datastore.infrastructure import DatastoreMapperMixin
from gumo.datastore.infrastructure import EntityKeyMapper


@dataclasses.dataclass(frozen=True)
class SampleEntity:
    key: EntityKey
    value: str


class SampleMapper(DatastoreMapperMixin):
    def to_datastore_entity(self, entity: SampleEntity) -> DatastoreMapperMixin.DatastoreEntity:
        pass

    def to_domain_entity(self, doc: DatastoreMapperMixin.DatastoreEntity) -> SampleEntity:
        pass


def test_datastore_mapper_mixin():
    mapper = SampleMapper()

    assert isinstance(mapper, SampleMapper)
    assert isinstance(mapper.entity_key_mapper, EntityKeyMapper)
    assert mapper.DatastoreEntity == datastore.Entity
