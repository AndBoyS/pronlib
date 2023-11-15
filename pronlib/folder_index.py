from abc import ABC, abstractmethod
from pathlib import Path
from typing import Type


def get_subfolders(path: Path) -> list[Path]:
    return [p for p in path.iterdir() if p.is_dir() and not p.name.startswith(".")]


class MediaChapter(ABC):
    @abstractmethod
    def __init__(self, chapter_path: Path) -> None:
        pass
    
    @abstractmethod
    def set_index(self, i: int) -> None:
        pass
    
    @abstractmethod
    def rename_to_temp(self) -> None:
        pass
    
    @abstractmethod
    def rename_update(self) -> None:
        pass
    
    

class FolderIndexer:
    def reindex_folders(self, media_path: Path, chapter_type: Type[MediaChapter], start_index: int = 1) -> None:
        chapters = [chapter_type(path) for path in get_subfolders(media_path)]
        
        for i, chapter in enumerate(chapters, start=start_index):
            chapter.set_index(i)
            chapter.rename_to_temp()
            
        for chapter in chapters:
            chapter.rename_update()

    def save_sauce(self) -> None:
        pass
