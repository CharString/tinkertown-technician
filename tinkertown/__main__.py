from pathlib import Path

import typer
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from .technician import download_cards, download_portraits, in_progress

app = typer.Typer()


class EventHandler(FileSystemEventHandler):
    def __init__(self, taskmap):
        super().__init__()
        self.taskmap = taskmap

    def on_modified(self, event):
        self.taskmap.get(event.src_path, lambda: None)()


@app.command()
def main(wineprefix: Path) -> None:
    """
    Tinkertown Technician -- Battlecry: Fix your Heartstone Deck Tracker

    Workaround for
     - https://github.com/HearthSim/Hearthstone-Deck-Tracker/issues/4234
    """
    try:
        path = next(wineprefix.glob('**/HearthstoneDeckTracker/Images'))
    except StopIteration:
        typer.echo(f'No decktracker found under {wineprefix}', err=True)
        raise typer.Exit(1)

    tasks = [
        ('CardImages', download_cards),
        ('CardPortraits', download_portraits),
    ]

    def make_task(d, f):
        def task():
            f(in_progress(path / d), path / d)
        return task

    handler = EventHandler(taskmap={
        str(path / d / '_inProgress'): make_task(d, f)
        for d, f in tasks
    })

    for p, f in handler.taskmap.items():
        f()

    observer = Observer()
    observer.schedule(handler, path, recursive=True)
    typer.echo(f'Monitoring {path} for changes. Stop with CTRL-C.')
    observer.start()
    try:
        observer.join()
    except KeyboardInterrupt:
        observer.stop()
        raise typer.Abort()


if __name__ == '__main__':
    app()
