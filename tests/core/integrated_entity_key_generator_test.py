from gumo.core import EntityKeyGenerator
from gumo.core.application.entity_key import KeyGenerateStyle
from gumo.core import EntityKey
from gumo.core import EntityKeyFactory


class TestEntityKeyGenerator:
    key_factory = EntityKeyFactory()

    def test_with_int_id(self):
        incomplete_key = self.key_factory.build_incomplete_key(kind='Sample')
        generator = EntityKeyGenerator(key_generate_style=KeyGenerateStyle.INT)

        key = generator.generate(incomplete_key=incomplete_key)
        assert isinstance(key, EntityKey)
        assert isinstance(key.name(), int)

        key2 = generator.generate(incomplete_key=incomplete_key)
        assert key != key2
        assert key.name() != key2.name()
