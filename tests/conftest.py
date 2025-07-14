import pytest
from bloblite.storage import Storage


@pytest.fixture
def storage(tmp_path):
    return Storage(base_path=tmp_path)
