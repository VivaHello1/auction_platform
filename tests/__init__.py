from core.dependency_injection import create_container
from tests.test_settings import test_settings

test_container = create_container(test_settings)
