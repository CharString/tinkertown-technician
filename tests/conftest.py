from pathlib import Path

import pytest
import typer

from tinkertown import technician

FIXTURE_DIR = Path(__file__).parent / 'fixtures'
TRACKER_ROOT = "drive_c/Program Files/Hearthstone Deck Tracker"


@pytest.fixture
def cache_xml():
    return FIXTURE_DIR / 'Cache.xml'


@pytest.fixture
def wineprefix():
    return FIXTURE_DIR / 'wineprefix'


@pytest.fixture(autouse=True)
def config(tmp_path, monkeypatch):
    monkeypatch.setattr(typer, "get_app_dir", lambda app_name: tmp_path)
    return tmp_path / "config.toml"


@pytest.fixture
def in_bad_path(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    return Path(tmp_path)


@pytest.fixture
def mock_decktracker(monkeypatch, wineprefix):
    tracker = wineprefix / TRACKER_ROOT / "Mock Decktracker"
    monkeypatch.setattr(technician, "HDT_EXE", tracker.name)
    return tracker
