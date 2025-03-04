from enum import Enum
from pathlib import Path
import tomllib


class MappingUtil:
    def __init__(self):
        self.config = MappingUtil.__load_config(self)

    @staticmethod
    def __load_config(self):
        with open(self.Directory.CONFIG.value, "rb") as config:
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
        SINGLE: str = NotImplemented
        COLLECTION: str = NotImplemented


if __name__ == "__main__":
    for path in MappingUtil.Directory:
        print(f"{path}: {path.value}")

    for FileType in MappingUtil.FileType:
        print(f"{FileType}: {FileType.value}")

    manager = MappingUtil()
    print(manager.config)
