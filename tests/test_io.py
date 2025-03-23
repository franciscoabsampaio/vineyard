import os
import pytest
from vinery.io import set_log_level


def test_set_log_level(monkeypatch):
    monkeypatch.delenv("VINE_LOG_LEVEL", raising=False)
    set_log_level("DEBUG")
    assert os.getenv("VINE_LOG_LEVEL") == "DEBUG"

    pytest.raises(ValueError, set_log_level, "INVALID_LOG_LEVEL")
