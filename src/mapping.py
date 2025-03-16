import tomllib

from enum import Enum
from pathlib import Path
from typing import Dict, Final


class MappingUtil:
    def __init__(self):
        self.config = MappingUtil.__load_config()

    @staticmethod
    def __load_config():
        with open(Directory.CONFIG.value, "rb") as config:
            config = tomllib.load(config)
            return config


class Directory(Enum):
    ROOT: Path = Path(__file__).resolve().parent
    COGS: Path = ROOT / "cogs"
    CONFIG: Path = ROOT / "config.toml"
    RESOURCE: Path = ROOT.parent / "res"
    DATABASE: Path = RESOURCE / "database.json"
    HEADERS: Path = RESOURCE / "headers.json"
    KEYWORDS: Path = RESOURCE / "keywords.json"


class FileType(Enum):
    COLLECTION: Final[Dict[str, str]] = {"dir": "collection", "ext": "collection"}
    IMAGE: Final[Dict[str, str]] = {"dir": "image", "ext": "png"}
    VIDEO: Final[Dict[str, str]] = {"dir": "video", "ext": "mp4"}
    GIF: Final[Dict[str, str]] = {"dir": "image", "ext": "gif"}


if __name__ == "__main__":
    for path in Directory:
        print(f"{path}: {path.value}")

    for FileType in FileType:
        print(f"{FileType}: {FileType.value}")

    manager = MappingUtil()
    print(manager.config)
