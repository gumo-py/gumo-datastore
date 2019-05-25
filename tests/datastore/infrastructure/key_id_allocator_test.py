from gumo.core.injector import injector
from gumo.core.application.entity_key import KeyIDAllocator
from gumo.core import EntityKeyFactory
from gumo.core.domain.entity_key import IncompleteKey

from gumo.datastore.infrastructure.key_id_allocator import DatastoreKeyIDAllocator
from gumo.datastore.infrastructure.key_id_allocator import CachedKeyIDAllocator


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


class TestCachedKeyIDAllocator:
    key_factory = EntityKeyFactory()

    def key_id_allocator(self) -> CachedKeyIDAllocator:
        return injector.get(CachedKeyIDAllocator)

    def tet_instance(self):
        assert isinstance(self.key_id_allocator(), CachedKeyIDAllocator)

    def test_cache(self):
        allocator = self.key_id_allocator()
        incomplete_key = self.key_factory.build_incomplete_key(kind='Sample')

        assert allocator._cache == {}

        allocator.allocate(incomplete_key=incomplete_key)
        assert len(allocator._cache) == 1
        assert len(allocator.fetch_cached_keys(incomplete_key)) == allocator.ALLOCATE_BATCH_SIZE - 1

        incomplete_with_parent_key = self.key_factory.build_incomplete_key(
            kind='Example',
            parent=self.key_factory.build(kind='Parent', name=123456)
        )
        allocator.allocate(incomplete_key=incomplete_with_parent_key)
        assert len(allocator._cache) == 2
        allocator.allocate(incomplete_key=incomplete_with_parent_key)
        assert len(allocator.fetch_cached_keys(incomplete_with_parent_key)) == allocator.ALLOCATE_BATCH_SIZE - 2
