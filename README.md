# Tinkertown Technician
![Battlecry: Fix your Hearthstone Deck Tracker](https://hearthcards.ams3.digitaloceanspaces.com/6d/3a/9a/1b/6d3a9a1b.png)

## Using

Just install it in an isolated environment with pipx.

```sh
pip install --user pipx
pipx install tinkertown-technician
```

And spin it up aand let it do it's thing while you're griefing Tavern ticket
noobs in the Arena, jamming meme decks in wild or cussing at Bob for not giving
you any synergy.


```sh
$ ttt --help
Usage: ttt [OPTIONS] [PATH]

  Tinkertown Technician -- Battlecry: Fix your Heartstone Deck Tracker

  Workaround for  - https://github.com/HearthSim/Hearthstone-Deck-
  Tracker/issues/4234

Arguments:
  [PATH]  [env var: WINEPREFIX;default: (dynamic)]

```

The `PATH` argument is optional, it will default to the `WINEPREFIX` from your
environment. And will fall back to either the path it remembered from the first
time it succeeded or `./`


You might have to add ~/.local/bin to your PATH.

## Developing

```sh
pip install --user pipx
pipx install pdm
pdm run dev
```
