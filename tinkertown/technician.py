import xml.etree.ElementTree as ET
from os import PathLike
from pathlib import Path
from typing import IO, Callable, Iterable, List, Union

from requests import get


def readcache(xml: Union[PathLike, IO]) -> Union[List, List[str]]:
    "Read a Cache.xml and return its strings"
    root = ET.parse(xml)
    return [el.text for el in root.findall('.//string')]


def in_progress(path: Path) -> Iterable[str]:
    return (
        f.name
        for f in (path / '_inProgress').iterdir()
        if f.is_file() and not f.stat().st_size
    )


def cardrender_url(card_img: str) -> str:
    locale, resolution = 'enUS', '512x'
    return ('https://art.hearthstonejson.com/v1/render/latest'
            f'/{locale}/{resolution}/{card_img}')


def cardportrait_url(card_img: str) -> str:
    return f'https://art.hearthstonejson.com/v1/256x/{card_img}'


def download(card_imgs: Iterable[str],
             destination: Path,
             url_mapper: Callable[[str], str],
             ) -> None:
    urls = ((url_mapper(card), (destination / card))
            for card in card_imgs
            if card and not (destination / card).exists()
            )
    for url, dest in urls:
        resp = get(url)
        if resp.ok:
            dest.open('wb+').write(resp.content)


def download_cards(card_imgs: Iterable[str],
                   destination: Path,
                   ) -> None:
    "Download card images shown on hover"
    return download(card_imgs, destination, url_mapper=cardrender_url)


def download_portraits(card_imgs: Iterable[str],
                       destination: Path,
                       ) -> None:
    "Download small images shown in Battlegrounds opponent boards"
    return download(card_imgs, destination, url_mapper=cardportrait_url)
