from tests import test_container


def test_schema_is_test():
    postgres_schema = test_container.config.POSTGRES_SCHEMA()
    assert postgres_schema == 'api_test'
