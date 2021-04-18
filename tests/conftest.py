from pathlib import Path

import pytest

FIXTURE_DIR = Path(__file__).parent / 'fixtures'


@pytest.fixture
def cache_xml():
    return FIXTURE_DIR / 'Cache.xml'


@pytest.fixture
def wineprefix():
    return FIXTURE_DIR / 'wineprefix'
