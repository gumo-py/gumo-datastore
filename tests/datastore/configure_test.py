import pytest
import os

from gumo.datastore.infrastructure.configuration import DatastoreConfiguration

from google.cloud import datastore
import google.auth.exceptions


class TestDatastoreConfiguration:
    def setup_method(self, method):
        self.env_vars = {}
        for k, v in os.environ.items():
            self.env_vars[k] = v

    def teardown_method(self, method):
        for k in os.environ.keys():
            if k not in self.env_vars:
                del os.environ[k]

        for k, v in self.env_vars.items():
            os.environ[k] = v

    def test_build_success_with_standard_configuration(self):
        if 'DATASTORE_EMULATOR_HOST' in os.environ:
            del os.environ['DATASTORE_EMULATOR_HOST']
        assert os.environ['GOOGLE_CLOUD_PROJECT'] is not None
        assert 'DATASTORE_EMULATOR_HOST' not in os.environ

        try:
            o = DatastoreConfiguration()

            assert o.google_cloud_project.value == os.environ['GOOGLE_CLOUD_PROJECT']
            assert not o.use_local_emulator
            assert o.emulator_host is None
            assert o.namespace is None
            assert isinstance(o.client, datastore.Client)
        except google.auth.exceptions.DefaultCredentialsError as e:
            # Depending on the environment, it is correct behavior for this test to fail.
            assert 'Could not automatically determine credentials.' in str(e)

    def test_build_success_with_emulator_configuration(self):
        assert os.environ['GOOGLE_CLOUD_PROJECT'] is not None
        assert os.environ['DATASTORE_EMULATOR_HOST'] is not None

        o = DatastoreConfiguration()

        assert o.google_cloud_project.value == os.environ['GOOGLE_CLOUD_PROJECT']
        assert o.use_local_emulator
        assert o.emulator_host == os.environ['DATASTORE_EMULATOR_HOST']
        assert o.namespace is None
        assert isinstance(o.client, datastore.Client)

    def test_build_failure_without_google_cloud_project_env_vars(self):
        if 'GOOGLE_CLOUD_PROJECT' in os.environ:
            del os.environ['GOOGLE_CLOUD_PROJECT']

        with pytest.raises(RuntimeError, match='"GOOGLE_CLOUD_PROJECT" is undefined'):
            DatastoreConfiguration()

    def test_build_failure_with_emulator_configuration_and_without_emulator_env_vars(self):
        if 'DATASTORE_EMULATOR_HOST' in os.environ:
            del os.environ['DATASTORE_EMULATOR_HOST']
        assert os.environ['GOOGLE_CLOUD_PROJECT'] is not None
        assert 'DATASTORE_EMULATOR_HOST' not in os.environ

        with pytest.raises(RuntimeError, match='env-var "DATASTORE_EMULATOR_HOST" must be present'):
            DatastoreConfiguration(
                use_local_emulator=True
            )

    def test_build_failure_with_emulator_host_mismatched(self):
        assert os.environ['GOOGLE_CLOUD_PROJECT'] is not None
        assert os.environ['DATASTORE_EMULATOR_HOST'] is not None

        with pytest.raises(RuntimeError,
                           match='Env-var "DATASTORE_EMULATOR_HOST" and self.emulator_host do not match.'):
            DatastoreConfiguration(
                use_local_emulator=True,
                emulator_host='example.localhost:12345'
            )
