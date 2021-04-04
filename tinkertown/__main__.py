from pathlib import Path

import typer

from .technician import (download_cards, download_portraits, in_progress,
                         readcache,)

app = typer.Typer()


@app.command()
def main(wineprefix: str) -> None:
    path = next(Path(wineprefix).glob('**/HearthstoneDeckTracker/Images'))

    card_path = path / 'CardImages'
    download_cards(readcache(card_path / 'Cache.xml'), card_path)

    port_path = path / 'CardPortraits'
    download_portraits(in_progress(port_path), port_path)


if __name__ == '__main__':
    app()
