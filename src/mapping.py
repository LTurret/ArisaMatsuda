import tomllib

from enum import Enum
from pathlib import Path

from src.types import Config


class MappingUtil:
    def __init__(self):
        self.config: Config = MappingUtil.__load_config()

    @staticmethod
    def __load_config():
        with open(Directory.CONFIG.value, "rb") as config:
            config = tomllib.load(config)
            return config


class Directory(Enum):
    ROOT = Path(__file__).resolve().parent
    COGS = ROOT / "cogs"
    CONFIG = ROOT / "config.toml"
    RESOURCE = ROOT.parent / "res"
    DATABASE = RESOURCE / "database.json"
    HEADERS = RESOURCE / "headers.json"
    KEYWORDS = RESOURCE / "keywords.json"


class FileType(Enum):
    COLLECTION = {"dir": "collection", "ext": "collection"}
    IMAGE = {"dir": "image", "ext": "png"}
    VIDEO = {"dir": "video", "ext": "mp4"}
    GIF = {"dir": "image", "ext": "gif"}


if __name__ == "__main__":
    for path in Directory:
        print(f"{path}: {path.value}")

    for theType in FileType:
        print(f"{theType}: {theType.value}")

    manager = MappingUtil()
    print(manager.config)
