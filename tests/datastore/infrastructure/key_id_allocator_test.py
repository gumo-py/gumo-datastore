from gumo.core.injector import injector
from gumo.core.application.entity_key import KeyIDAllocator
from gumo.core import EntityKeyFactory
from gumo.core.domain.entity_key import IncompleteKey
from gumo.datastore.infrastructure.key_id_allocator import DatastoreKeyIDAllocator


class TestKeyIDAllocator:
    _key_id_allocator = None

    @property
    def key_id_allocator(self) -> KeyIDAllocator:
        if self._key_id_allocator is None:
            injector.binder.bind(KeyIDAllocator, to=DatastoreKeyIDAllocator)
            self._key_id_allocator = injector.get(KeyIDAllocator)

        return self._key_id_allocator

    def test_allocate_key(self):
        incomplete_key = EntityKeyFactory().build_incomplete_key(kind='Sample')
        assert isinstance(incomplete_key, IncompleteKey)

        allocated_key = self.key_id_allocator.allocate(incomplete_key=incomplete_key)
        assert allocated_key.kind() == 'Sample'
        assert isinstance(allocated_key.name(), int)
