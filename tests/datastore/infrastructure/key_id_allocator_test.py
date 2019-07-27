from gumo.core.injector import injector
from gumo.core import EntityKeyFactory
from gumo.core.domain.entity_key import IncompleteKey

from gumo.datastore.infrastructure.key_id_allocator import DatastoreKeyIDAllocator


class TestKeyIDAllocator:
    def build_key(self, kind: str):
        return EntityKeyFactory().build_incomplete_key(kind=kind)

    def build_allocator(self) -> DatastoreKeyIDAllocator:
        return injector.get(DatastoreKeyIDAllocator)

    def test_allocate_key(self):
        incomplete_key = self.build_key(kind='Sample')
        assert isinstance(incomplete_key, IncompleteKey)
        allocator = self.build_allocator()

        allocated_key = allocator.allocate(incomplete_key=incomplete_key)
        assert allocated_key.kind() == 'Sample'
        assert isinstance(allocated_key.name(), int)

    def test_allocate_keys_with_cache(self):
        incomplete_key = self.build_key(kind='Sample')
        allocator = self.build_allocator()

        assert allocator._cache == {}
        allocator.allocate(incomplete_key)
        assert len(allocator._cache) == 1
        assert len(allocator._cache[incomplete_key]) == allocator.ALLOCATE_BATCH_SIZE - 1
        keys = allocator.allocate_keys(incomplete_key, num_keys=2)
        assert len(keys) == 2
        assert len(allocator._cache[incomplete_key]) == allocator.ALLOCATE_BATCH_SIZE - 3

        allocator.allocate(self.build_key(kind='AnotherKind'))
        assert len(allocator._cache) == 2

    def test_allocate_key_with_parent(self):
        incomplete_key = EntityKeyFactory().build_incomplete_key(
            kind='Sample',
            parent=EntityKeyFactory().build(kind='Parent', name=123456)
        )
        assert incomplete_key.key_literal() == "IncompleteKey('Parent', 123456, Sample)"
        allocator = self.build_allocator()
        allocated_key = allocator.allocate(incomplete_key=incomplete_key)
        assert allocated_key.kind() == 'Sample'
        assert isinstance(allocated_key.name(), int)

        assert allocated_key.parent().kind() == 'Parent'
        assert allocated_key.parent().name() == 123456
