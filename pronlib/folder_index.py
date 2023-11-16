from abc import ABC, abstractmethod
import json
from pathlib import Path
import re

from natsort import natsorted


def get_subfolders(path: Path) -> list[Path]:
    return [p for p in path.iterdir() if p.is_dir() and not p.name.startswith(".")]


def get_content_subfiles(path: Path) -> list[Path]:
    return [p for p in path.iterdir() if p.name.lower() != "meta.json" and not p.name.startswith(".")]


class Media(ABC):
    path: Path
    title: str
    index: int
    
    @abstractmethod
    def __init__(self, chapter_path: Path, index: int) -> None:
        pass

    @abstractmethod
    def rename_to_temp(self) -> None:
        pass
    
    @property
    @abstractmethod
    def full_title(self) -> str:
        pass
    
    def rename_update(self) -> None:
        new_path = self.path.with_name(f'{self.full_title}{self.path.suffix}')
        self.path = self.path.rename(new_path)



class Video(Media):
    def __init__(self, path: Path, index: int) -> None:
        self.path = path
        self.index = index
        self.title = self.path.stem.replace("_temp", "")
        self.title = re.sub(r"^\d+", "", self.title).strip()

    @property
    def full_title(self) -> str:
        return f"{self.index} {self.title}".strip()

    def rename_to_temp(self) -> None:
        temp_name = f"{self.full_title}_temp{self.path.suffix}"
        temp_path = self.path.with_name(temp_name)
        self.path = self.path.rename(temp_path)


class PhotoFolder(Media):
    def __init__(self, path: Path, index: int) -> None:
        self.path = path
        self.index = index
        self.title = self.path.stem.replace("_temp", "")
        self.title = re.sub(r"^\d+", "", self.title)
        
        if not self.path.is_dir():
            raise ValueError(f"{self.path} is not a dir, but its expected to be")

        self.artist_name = None
        artist_ptrn = re.compile(r"\[(.+)\]$")
        artist_match = artist_ptrn.search(self.title)
        if artist_match is not None:
            self.artist_name = artist_match.group(1).title()

        self.title = artist_ptrn.sub("", self.title).strip()

    @property
    def full_title(self) -> str:
        full_title = f"{self.index} {self.title}".strip()
        if self.artist_name is not None:
            full_title = f"{full_title} [{self.artist_name}]"

        return full_title
    
    def rename_to_temp(self) -> None:
        temp_path = self.path.with_name(f"{self.path.name}_temp")
        self.path = self.path.rename(temp_path)

    def rename_update(self) -> None:
        new_path = self.path.with_name(self.full_title)
        self.path = self.path.rename(new_path)


class MediaChapter(ABC):
    path: Path
    title: str
    index: int
    count: int
    media_list: list[Media]

    @abstractmethod
    def __init__(self, chapter_path: Path, index: int) -> None:
        pass

    def rename_to_temp(self) -> None:
        temp_path = self.path.with_name(f"{self.full_title}_temp")
        self.path = self.path.rename(temp_path)

    def rename_update(self) -> None:
        new_path = self.path.with_name(self.full_title)
        self.path = self.path.rename(new_path)

    @property
    def full_title(self) -> str:
        return f"{self.index} {self.title} ({self.count})".strip()


class VideoChapter(MediaChapter):
    def __init__(self, chapter_path: Path, index: int) -> None:
        self.path = chapter_path
        self.index = index

        if not self.path.is_dir():
            raise ValueError(f"{self.path} is not a dir, but its expected to be")

        self.title = self.path.stem.replace("_temp", "")
        self.title = re.sub(r"^\d+", "", self.title)
        self.title = re.sub(r"\(\d+\)$", "", self.title).strip()

        media_paths = natsorted(get_content_subfiles(self.path))
        self.media_list = [Video(p, i) for i, p in enumerate(media_paths, start=1)]
        self.count = len(self.media_list)


class PhotoChapter(MediaChapter):
    def __init__(self, chapter_path: Path, index: int) -> None:
        self.path = chapter_path
        self.index = index

        if not self.path.is_dir():
            raise ValueError(f"{self.path} is not a dir, but its expected to be")

        self.title = self.path.stem.replace("_temp", "")
        self.title = re.sub(r"^\d+", "", self.title)
        self.title = re.sub(r"\(\d+\)$", "", self.title).strip()

        media_paths = natsorted(get_content_subfiles(self.path))
        self.media_list = [PhotoFolder(p, i) for i, p in enumerate(media_paths, start=1)]
        self.count = len(self.media_list)


def reindex_folders(chapters: list[MediaChapter]) -> None:
    
    for chapter in chapters:
        for media in chapter.media_list:
            media.rename_to_temp()
        for media in chapter.media_list:
            media.rename_update()

    for chapter in chapters:
        chapter.rename_to_temp()
    for chapter in chapters:
        chapter.rename_update()


def save_sauce(chapters: list[MediaChapter], save_path: Path | str) -> None:
    sauce = {f"{chapter.index} {chapter.title}": chapter.count for chapter in chapters}
    with open(save_path, "w", encoding="utf8") as f:
        json.dump(sauce, f)
