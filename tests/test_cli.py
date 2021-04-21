"""Tests the `ttt` cli"""

import os
import shutil
from pathlib import Path
from unittest.mock import Mock

import pytest
from typer.testing import CliRunner

from tinkertown import __main__

runner = CliRunner(mix_stderr=False)


@pytest.fixture(autouse=True)
def watchdog_observer(monkeypatch):
    observer = Mock()
    monkeypatch.setattr(__main__, "Observer", observer)
    observer.return_value.join.side_effect = KeyboardInterrupt()
    return observer


@pytest.fixture(autouse=True)
def decktracker_mgmt(monkeypatch):
    start, running = Mock(), Mock()
    monkeypatch.setattr(__main__, "start_decktracker", start)
    monkeypatch.setattr(__main__, "running_decktracker", running)
    return start, running


def test_passing_in_path(wineprefix):
    path = str(wineprefix)
    result = runner.invoke(__main__.app, [path])
    assert f"Monitoring {path}" in result.stdout
    assert result.exit_code == 0


def test_fallback_to_wineprefix_from_environ(wineprefix, monkeypatch):
    path = str(wineprefix)
    monkeypatch.setattr(os, "environ", {"WINEPREFIX": path})
    result = runner.invoke(__main__.app)
    assert f"Monitoring {path}" in result.stdout
    assert result.exit_code == 0


def test_invalid_path(in_bad_path):
    result = runner.invoke(__main__.app)
    assert "No decktracker" in result.stderr
    assert result.exit_code == 1


def test_saves_path_to_config(wineprefix: Path, config: Path):
    assert not config.is_file()
    result = runner.invoke(__main__.app, [str(wineprefix)])
    assert result.exit_code == 0
    assert config.is_file()
    conf = config.open().read()
    assert f'path = "{wineprefix}"' in conf


def test_doesnt_save_bad_path(in_bad_path, config):
    result = runner.invoke(__main__.app)
    assert result.exit_code == 1
    assert not config.is_file()


def test_uses_path_from_config(in_bad_path, wineprefix, config: Path):
    with config.open('w+') as f:
        f.write(f'path = "{wineprefix}"\n')
    result = runner.invoke(__main__.app)
    assert result.exit_code == 0
    assert f"Monitoring {wineprefix}" in result.stdout


def test_doesnt_overwrite_path(in_bad_path, wineprefix, config: Path):
    shutil.copytree(wineprefix, in_bad_path / "copied_prefix")
    with config.open("w+") as f:
        f.write(f'path = "{wineprefix}"\n')
    result = runner.invoke(__main__.app, ["./"])
    assert result.exit_code == 0
    assert str(wineprefix) not in result.stdout
    assert "copied_prefix" in result.stdout
    conf = config.open().read()
    assert str(in_bad_path) not in conf
    assert str(wineprefix) in conf


def test_ctrl_c_exits_cleanly(watchdog_observer, wineprefix):
    watchdog_observer.return_value.join.side_effect = KeyboardInterrupt()
    result = runner.invoke(__main__.app, [str(wineprefix)])
    assert result.exit_code == 0


def test_empty_evenhandler():
    handler = __main__.EventHandler({})
    assert handler.on_modified(Mock()) is None


def test_relaunch_eaunches_decktracker(decktracker_mgmt):
    start, running = decktracker_mgmt
    running.return_value = None
    runner.invoke(__main__.app, ['--relaunch'])
    start.assert_called_once_with(Path("."))


def test_relaunch_fails_when_no_decktracker_found(decktracker_mgmt):
    start, running = decktracker_mgmt
    running.return_value = None
    start.side_effect = RuntimeError('Error')
    result = runner.invoke(__main__.app, ['--relaunch'])
    assert result.exit_code == 2


def test_relaunch_doesnt_launch_when_already_runs(decktracker_mgmt):
    start, running = decktracker_mgmt
    runner.invoke(__main__.app, ['--relaunch'])
    running.assert_called()
    start.assert_not_called()


def test_relaunch_zombie(decktracker_mgmt, watchdog_observer):
    start, running = decktracker_mgmt
    tracker = Mock()
    running.return_value = tracker
    watchdog_observer.return_value.join.side_effect = [
        None,
        KeyboardInterrupt(),
    ]
    tracker.status.return_value = "zombie"
    runner.invoke(__main__.app, ['--relaunch'])
    start.assert_called_once()
