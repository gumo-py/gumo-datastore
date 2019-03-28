import pytest

from gumo.datastore._configuration import ConfigurationFactory
from gumo.datastore.domain.configuration import DatastoreConfiguration


def test_configuration_factory_build():
    o = ConfigurationFactory.build(
        use_local_emulator='yes',
        emulator_host='localhost:8080',
        namespace='test',
    )

    assert o == DatastoreConfiguration(
        use_local_emulator=True,
        emulator_host='localhost:8080',
        namespace='test',
    )


def test_configuration_factory_build_failed():
    with pytest.raises(ValueError):
        ConfigurationFactory.build(
            use_local_emulator='yes',
            emulator_host=None,
            namespace='test',
        )
