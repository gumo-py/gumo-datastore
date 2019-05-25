from typing import Optional
from injector import inject

from gumo.core import GumoConfiguration
from gumo.core.injector import injector

from gumo.core.application.entity_key import KeyIDAllocator
from gumo.core.domain.entity_key import NoneKey
from gumo.core.domain.entity_key import EntityKey
from gumo.core.domain.entity_key import EntityKeyFactory
from gumo.core.domain.entity_key import IncompleteKey

from gumo.datastore.infrastructure.repository import DatastoreClientFactory

from google.cloud import datastore


class DatastoreKeyIDAllocator(KeyIDAllocator):
    _datastore_client = None

    @inject
    def __init__(
            self,
            gumo_config: GumoConfiguration,
            entity_key_factory: EntityKeyFactory,
    ):
        self._gumo_config = gumo_config
        self._entity_key_factory = entity_key_factory

    @property
    def datastore_client(self) -> datastore.Client:
        if self._datastore_client is None:
            factory = injector.get(DatastoreClientFactory)  # type: DatastoreClientFactory
            self._datastore_client = factory.build()

        return self._datastore_client

    def _to_datastore_key(self, incomplete_key: IncompleteKey) -> Optional[datastore.Key]:
        if incomplete_key is None or isinstance(incomplete_key, NoneKey):
            return None

        project = self._gumo_config.google_cloud_project.value
        datastore_key = datastore.Key(*incomplete_key.flat_pairs(), project=project)

        return datastore_key

    def _to_entity_key(self, datastore_key: Optional[datastore.Key]) -> EntityKey:
        if datastore_key is None:
            return NoneKey.get_instance()

        entity_key = EntityKeyFactory().build_from_pairs(pairs=datastore_key.path)
        return entity_key

    def allocate(self, incomplete_key: IncompleteKey) -> EntityKey:
        datastore_key = self._to_datastore_key(incomplete_key=incomplete_key)
        allocated_keys = self.datastore_client.allocate_ids(incomplete_key=datastore_key, num_ids=10)

        keys = [self._to_entity_key(datastore_key=key) for key in allocated_keys]
        return keys[0]
