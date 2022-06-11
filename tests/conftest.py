import sys
from pathlib import Path

import pytest

CWD = Path(__file__).resolve().parent
code_dir = CWD / '../src'
sys.path.append(str(code_dir))


def pytest_configure(config):
    """Called at the start of the entire test run"""
    pass


@pytest.fixture()
def fake_thing():
    return 1
