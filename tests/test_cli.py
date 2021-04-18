"""Tests the `ttt` cli"""

import os
from unittest.mock import Mock

from typer.testing import CliRunner

from tinkertown import __main__

runner = CliRunner(mix_stderr=False)


def test_passing_in_path(wineprefix, monkeypatch):
    path = str(wineprefix)
    monkeypatch.setattr(__main__, "Observer", Mock())
    result = runner.invoke(__main__.app, [path])
    assert f"Monitoring {path}" in result.stdout
    assert result.exit_code == 0


def test_fallback_to_wineprefix_from_environ(wineprefix, monkeypatch):
    path = str(wineprefix)
    monkeypatch.setattr(__main__, "Observer", Mock())
    monkeypatch.setattr(os, "environ", {"WINEPREFIX": path})
    result = runner.invoke(__main__.app)
    assert f"Monitoring {path}" in result.stdout
    assert result.exit_code == 0


def test_invalid_path(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    result = runner.invoke(__main__.app)
    assert "No decktracker" in result.stderr
    assert result.exit_code == 1
