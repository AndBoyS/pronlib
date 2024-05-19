from abc import ABC, abstractmethod
from pathlib import Path
import re
from typing import Type

from natsort import natsorted

from src.const import META_NAME
from ..utils import load_json


def get_subfolders(path: Path) -> list[Path]:
    return [p for p in path.iterdir() if p.is_dir() and not p.name.startswith(".")]


def get_content_subfiles(path: Path) -> list[Path]:
    return [p for p in path.iterdir() if p.name.lower() != META_NAME and not p.name.startswith(".")]


index_ptrn = re.compile(r"^\d+")


def extract_index(path_name: str) -> int | None:
    index = None
    index_match = index_ptrn.search(path_name)
    if index_match is not None:
        index = int(index_match.group(0))
    return index


class Media(ABC):
    path: Path
    title: str
    index: int | None
    meta: dict[str, str] | None = None

    @abstractmethod
    def __init__(self, chapter_path: Path) -> None:
        pass

    @abstractmethod
    def rename_to_temp(self) -> None:
        pass

    @property
    @abstractmethod
    def full_title(self) -> str:
        pass

    @abstractmethod
    def rename_update(self, index: int) -> None:
        pass

    def __repr__(self) -> str:
        return f"{type(self).__name__}(title={self.title})"


class Video(Media):
    def __init__(self, path: Path) -> None:
        self.path = path
        self.index = extract_index(self.path.name)
        self.title = self.path.stem.replace("_temp", "")
        self.title = index_ptrn.sub("", self.title).strip()

    @property
    def full_title(self) -> str:
        return f"{self.index} {self.title}".strip()

    def rename_to_temp(self) -> None:
        temp_name = f"{self.full_title}_temp{self.path.suffix}"
        temp_path = self.path.with_name(temp_name)
        self.path = self.path.rename(temp_path)

    def rename_update(self, index: int) -> None:
        self.index = index
        new_path = self.path.with_name(f"{self.full_title}{self.path.suffix}")
        self.path = self.path.rename(new_path)


class PhotoFolder(Media):
    artist_ptrn = re.compile(r"\[(.+)\]")

    def __init__(self, path: Path) -> None:
        self.path = path
        self.index = extract_index(self.path.name)
        self.title = self.path.stem.replace("_temp", "")
        self.title = index_ptrn.sub("", self.title)

        if not self.path.is_dir():
            raise ValueError(f"{self.path} is not a dir, but its expected to be")

        self.artist_name = None

        artist_match = self.artist_ptrn.search(self.title)
        if artist_match is not None:
            self.artist_name = artist_match.group(1).title()

        self.title = self.artist_ptrn.sub("", self.title).strip()

        self.meta = None
        if self.meta_path.exists():
            self.meta = load_json(self.meta_path)

    @property
    def meta_path(self) -> Path:
        return self.path / META_NAME

    @property
    def full_title(self) -> str:
        full_title = f"{self.index} {self.title}".strip()
        if self.artist_name is not None:
            full_title = f"{full_title} [{self.artist_name}]"

        return full_title

    def rename_to_temp(self) -> None:
        temp_path = self.path.with_name(f"{self.path.name}_temp")
        self.path = self.path.rename(temp_path)

    def rename_update(self, index: int) -> None:
        self.index = index
        new_path = self.path.with_name(self.full_title)
        self.path = self.path.rename(new_path)


class MediaChapter(ABC):
    path: Path
    title: str
    index: int | None
    count: int | None
    media_cls: Type[Media]
    media_list: list[Media]
    counter_ptrn = re.compile(r"\((\d+)\)$")

    def __init__(self, chapter_path: Path) -> None:
        self.path = chapter_path

        if not self.path.is_dir():
            raise ValueError(f"{self.path} is not a dir, but its expected to be")

        self.index = extract_index(self.path.name)
        self.title = self.extract_title()
        self.count = self.extract_count()

        media_paths = natsorted(get_content_subfiles(self.path))
        self.media_list = [self.media_cls(p) for p in media_paths]

    def extract_count(self) -> int | None:
        count = None
        count_match = self.counter_ptrn.search(self.path.stem)
        if count_match is not None:
            count = int(count_match.group(1))
        return count

    def extract_title(self) -> str:
        title = self.path.stem.replace("_temp", "")
        title = index_ptrn.sub("", title)
        title = self.counter_ptrn.sub("", title).strip()
        return title

    def rename_to_temp(self) -> None:
        temp_path = self.path.with_name(f"{self.full_title}_temp")
        self.path = self.path.rename(temp_path)

    def rename_update(self, index: int) -> None:
        self.count = len(self.media_list)
        self.index = index

        new_path = self.path.with_name(self.full_title)
        self.path = self.path.rename(new_path)

    @property
    def full_title(self) -> str:
        return f"{self.index} {self.title} ({self.count})".strip()

    def __repr__(self) -> str:
        return f"{type(self).__name__}(title={self.title})"


class VideoChapter(MediaChapter):
    media_cls = Video


class PhotoChapter(MediaChapter):
    media_cls = PhotoFolder


def reindex_folders(chapters: list[MediaChapter], start_index: int = 1) -> None:
    for chapter in chapters:
        for media in chapter.media_list:
            media.rename_to_temp()
        for i, media in enumerate(chapter.media_list, start=1):
            media.rename_update(i)

    for chapter in chapters:
        chapter.rename_to_temp()
    for i, chapter in enumerate(chapters, start=start_index):
        chapter.rename_update(i)


def get_sauce(chapters: list[MediaChapter]) -> dict[str, int | None]:
    sauce = {f"{chapter.title}": chapter.count for chapter in chapters}
    return sauce
