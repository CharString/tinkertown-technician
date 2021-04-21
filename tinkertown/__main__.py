from pathlib import Path
from typing import Any, MutableMapping

import toml
import typer
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from .technician import (download_cards, download_portraits, in_progress,
                         running_decktracker, start_decktracker,)

APP_NAME = "tinkertown-technician"
app = typer.Typer()


class EventHandler(FileSystemEventHandler):
    def __init__(self, taskmap):
        super().__init__()
        self.taskmap = taskmap

    def on_modified(self, event):
        self.taskmap.get(event.src_path, lambda: None)()


def config_path() -> Path:
    app_dir = Path(typer.get_app_dir(APP_NAME))
    if not app_dir.exists():
        app_dir.mkdir()  # pragma: no cover
    return app_dir / "config.toml"


def default_path() -> str:
    config: MutableMapping[str, Any] = dict()
    config_file = config_path()
    if config_file.is_file():
        config = toml.load(config_file)
    return config.get('path', '.')


def safe_config(config: dict) -> None:
    with config_path().open('w+') as f:
        toml.dump(config, f)


@app.command()
def main(
    path: Path = typer.Argument(default_path, envvar='WINEPREFIX'),
    relaunch: bool = typer.Option(
        False,
        help="EXPERIMENTAL relaunch Decktracker when it hangs",
    ),
) -> None:
    """
    Tinkertown Technician -- Battlecry: Fix your Heartstone Deck Tracker

    Workaround for
     - https://github.com/HearthSim/Hearthstone-Deck-Tracker/issues/4234
    """
    try:
        image_path = next(path.glob('**/HearthstoneDeckTracker/Images'))
    except StopIteration:
        typer.echo(f'No decktracker found under {path}', err=True)
        raise typer.Exit(1)

    if default_path() == '.':
        safe_config({'path': str(path.absolute())})

    tasks = [
        ('CardImages', download_cards),
        ('CardPortraits', download_portraits),
    ]

    def make_task(d, f):
        def task():
            f(in_progress(image_path / d), image_path / d)

        return task

    handler = EventHandler(taskmap={
        str(image_path / d / '_inProgress'): make_task(d, f)
        for d, f in tasks
    })

    for p, f in handler.taskmap.items():
        f()

    observer = Observer()
    observer.schedule(handler, image_path, recursive=True)
    typer.echo(f'Monitoring {image_path} for changes. Stop with CTRL-C.')
    observer.start()
    try:
        if relaunch:
            tracker = running_decktracker() or start_decktracker(path)
        while True:
            observer.join(10)
            if relaunch and tracker.status() == "zombie":
                tracker.terminate()
                tracker = start_decktracker(path)
    except RuntimeError as e:
        typer.echo(e, err=True)
        raise typer.Exit(2)
    except KeyboardInterrupt:
        observer.stop()
        raise typer.Exit()


if __name__ == '__main__':
    app()
