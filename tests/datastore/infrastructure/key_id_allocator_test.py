from gumo.core.injector import injector
from gumo.core.application.entity_key import KeyIDAllocator
from gumo.core import EntityKeyFactory
from gumo.core.domain.entity_key import IncompleteKey
from gumo.datastore.infrastructure.key_id_allocator import DatastoreKeyIDAllocator


class TestEntityKeyGenerator:
    _entity_key_generator = None

    @property
    def entity_key_generator(self) -> KeyIDAllocator:
        if self._entity_key_generator is None:
            injector.binder.bind(KeyIDAllocator, to=DatastoreKeyIDAllocator)
            self._entity_key_generator = injector.get(KeyIDAllocator)

        return self._entity_key_generator

    def test_allocate_key(self):
        incomplete_key = EntityKeyFactory().build_incomplete_key(kind='Sample')
        assert isinstance(incomplete_key, IncompleteKey)

        allocated_key = self.entity_key_generator.allocate(incomplete_key=incomplete_key)
        assert allocated_key.kind() == 'Sample'
        assert isinstance(allocated_key.name(), int)
