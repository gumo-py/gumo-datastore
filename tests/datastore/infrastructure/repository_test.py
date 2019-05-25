import dataclasses

from gumo.core import EntityKey
from gumo.core import EntityKeyFactory

from gumo.datastore.infrastructure import DatastoreRepositoryMixin
from gumo.datastore.infrastructure import DatastoreMapperMixin
from gumo.datastore.infrastructure import DatastoreEntity


@dataclasses.dataclass(frozen=True)
class SampleEntity:
    KIND = 'SampleEntity'

    key: EntityKey
    value: str


class SampleMapper(DatastoreMapperMixin):
    def to_datastore_entity(self, entity: SampleEntity) -> DatastoreEntity:
        e = DatastoreEntity(key=self.entity_key_mapper.to_datastore_key(entity.key))
        e.update({
            'value': entity.value
        })
        return e

    def to_domain_entity(self, doc: DatastoreEntity) -> SampleEntity:
        return SampleEntity(
            key=self.entity_key_mapper.to_entity_key(datastore_key=doc.key),
            value=doc.get('value')
        )


class TestRepository(DatastoreRepositoryMixin):
    KIND = SampleEntity.KIND

    def __init__(self):
        self.sample_mapper = SampleMapper()

    def save(self, entity: SampleEntity):
        datastore_entity = self.sample_mapper.to_datastore_entity(entity=entity)
        self.datastore_client.put(datastore_entity)

    def fetch(self, key: EntityKey) -> SampleEntity:
        doc = self.datastore_client.get(key=self.entity_key_mapper.to_datastore_key(entity_key=key))
        entity = self.sample_mapper.to_domain_entity(doc=doc)
        return entity

    def count(self):
        query = self.datastore_client.query(kind=self.KIND)
        query.keys_only()

        return len(list(query.fetch()))


class TestDatastoreRepository:
    repository = TestRepository()

    def build_entity(self, value: str = 'sample value') -> SampleEntity:
        return SampleEntity(
            key=EntityKeyFactory().build_for_new(kind=SampleEntity.KIND),
            value=value,
        )

    def test_repository(self):
        assert self.repository is not None
        assert isinstance(self.repository, TestRepository)

    def test_save_success(self):
        prev_count = self.repository.count()
        entity = self.build_entity()
        self.repository.save(entity=entity)
        assert self.repository.count() == prev_count + 1

    def test_fetch_success(self):
        entity = self.build_entity()
        self.repository.save(entity=entity)

        o = self.repository.fetch(key=entity.key)
        assert isinstance(o, entity.__class__)
        assert o.key == entity.key
        assert o.value == entity.value
