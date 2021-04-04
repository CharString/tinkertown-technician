from pathlib import Path

from tinkertown.technician import (download_cards, download_portraits,
                                   in_progress, readcache,)

PWD = Path(__file__).parent
CARDS = [
    'BT_723.png',
    'BT_252.png',
    'SCH_248.png',
]


def test_read():
    with (PWD / 'Cache.xml').open() as f:
        assert list(readcache(f)) == CARDS


def test_in_progress():
    imgs = list(in_progress(PWD))
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
