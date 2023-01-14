from dataclasses import dataclass


@dataclass
class Resources:
    start: str
    help: str


@dataclass
class Constants:
    resources: Resources


def get_resources() -> Resources:
    items = {}
    names = {"start": "start.html", "help": "help.html"}
    for name, filename in names.items():
        with open(f"resources/{filename}") as f:
            items[name] = f.read()
    return Resources(**items)


constants = Constants(get_resources())
