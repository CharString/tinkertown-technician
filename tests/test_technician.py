import time
from subprocess import Popen

import pytest
from psutil import Process

from tinkertown import technician
from tinkertown.technician import (download_cards, download_portraits,
                                   in_progress, readcache,)

CARDS = [
    'BT_723.png',
    'BT_252.png',
    'SCH_248.png',
]


def test_readcache(cache_xml):
    with cache_xml.open() as f:
        assert list(readcache(f)) == CARDS


def test_in_progress(wineprefix):
    card_images_dir = next(wineprefix.glob('**/Images/CardImages'))
    imgs = list(in_progress(card_images_dir))
    assert 'not_empty.png' not in imgs
    assert 'test.png' in imgs


def test_download_cards(tmp_path):
    download_cards(CARDS, tmp_path)
    for img in CARDS:
        assert (tmp_path / img).stat().st_size


def test_download_portraits(tmp_path):
    bgs_cards = ['BAR_073.jpg', 'BGS_014.jpg']
    download_portraits(bgs_cards, tmp_path)
    for img in bgs_cards:
        assert (tmp_path / img).stat().st_size


def test_running_decktracker_finds_nothing(mock_decktracker):
    assert technician.running_decktracker() is None


def test_running_decktracker_finds_tracker(mock_decktracker):
    p = Popen([str(mock_decktracker)])
    time.sleep(0.5)  # Wait for proctitle to be set
    tracker = technician.running_decktracker()
    try:
        assert Process(pid=p.pid).name() == mock_decktracker.name
        assert tracker
    finally:
        p.terminate()


def test_start_decktracker(wineprefix, mock_decktracker):
    tracker = technician.start_decktracker(wineprefix, wine='python')
    assert tracker.status() in ('sleeping', 'running')
    tracker.terminate()


def test_start_decktracker_raises_runtimeerror(wineprefix):
    "It should raise RuntimeError if exe not found"
    with pytest.raises(RuntimeError):
        technician.start_decktracker(wineprefix)


def test_start_decktracker_searches_both_names(tmp_path):
    "The executable has changed names over the years"
    with pytest.raises(RuntimeError):
        technician.start_decktracker(tmp_path)
    for exe in [
            "Hearthstone Deck Tracker.exe",
            "HearthstoneDeckTracker.exe",
    ]:
        f = (tmp_path / exe)
        f.open('w').close()
        process = technician.start_decktracker(tmp_path, 'echo')
        assert process.pid
        f.unlink()
