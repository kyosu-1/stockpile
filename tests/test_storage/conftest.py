import pytest

from stockpile.storage.sqlite import SQLiteStorage


@pytest.fixture
def storage(tmp_path):
    s = SQLiteStorage(tmp_path / "test.db")
    yield s
    s.close()
