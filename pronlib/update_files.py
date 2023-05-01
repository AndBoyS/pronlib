import re
from abc import ABC, abstractmethod

from natsort import natsorted


class FolderName:

    def __init__(self, folder_name: str):
        folder_name = folder_name.strip('_ ')

        match = re.match(r'\d+', folder_name)
        assert match is not None, f'Didnt find index in folder: {folder_name}'
        index = int(match.group(0))
        folder_name = folder_name[match.end():].strip()

        total = None
        match = re.search(r'\(\d+\)', folder_name)
        if match:
            total = int(match.group(0)[1:-1])
            folder_name = self.remove_range_from_str(
                folder_name,
                match.start(),
                match.end(),
            )
            folder_name = re.sub(r' +', ' ', folder_name).strip()

        match = re.search(r'\[.+?\]', folder_name)
        artist = None
        if match:
            artist = match.group(0)[1:-1].strip()
            folder_name = self.remove_range_from_str(
                folder_name,
                match.start(),
                match.end(),
            )
            folder_name = re.sub(r' +', ' ', folder_name).strip()

        self.index: int = index
        self.title: str = folder_name
        self.artist: str = artist
        self.total: int = total

    @staticmethod
    def remove_range_from_str(s: str, start: int, end: int) -> str:
        return s[:start] + s[end:]

    def __str__(self):
        title = ''
        if self.title:
            title = f' {self.title}'

        artist = ''
        if self.artist:
            artist = f' [{self.artist}]'

        total = ''
        if self.total:
            total = f' ({self.total})'

        return f'{self.index}{title}{artist}{total}'

    def __repr__(self):
        return f'FolderName({str(self)})'


class FileUpdater(ABC):
    '''
    Обновляет индексы и счетчики в названиях папок
    '''

    childs_are_folders = None  # Должно быть определено наследующим классом

    def __init__(self, base_dir, start_index=0):
        '''
        start_index - с какого индекса начинается нумерация основных папок
        '''
        self.base_dir = base_dir
        self.main_folders = self.get_subfolders(base_dir)
        self.start_index = start_index
    
    def update(self, folders=None, start_index=None, recursive_update=True):
        
        if folders is None:
            folders = self.main_folders

        if start_index is None:
            start_index = self.start_index
        
        temp_folders = []

        for cur_id, folder in enumerate(folders, start=start_index):
            name = FolderName(folder.name)
            name.index = cur_id

            json_fps = folder.glob('*.json')
            if not recursive_update and folder / 'meta.json' in json_fps:
                from pronlib.update_meta import load_json

                artist_name = load_json(folder / 'meta.json')['artist']
                name.artist = artist_name.title()

            # Обновление подпапок
            if recursive_update:
                child_files = self.get_subfolders(folder)
                self.update_child_files(child_files)
                name.total = len(child_files)

            # Сначала переименовываем в "новое имя_", потом в "новое имя"
            # чтобы избежать конфликтов, когда файл "новое имя" уже есть
            temp_folders.append(folder.rename(folder.parent / (str(name)+'_')))

        for folder in temp_folders:
            folder.rename(folder.parent / folder.name[:-1])
            
    def get_subfolders(self, base_dir=None, childs_are_folders=None):
        '''
        Получить список папок в директории
        '''
        if base_dir is None:
            base_dir = self.base_dir

        if childs_are_folders is None:
            childs_are_folders = self.childs_are_folders

        # Файлы являются папками
        if childs_are_folders:
            folders = [path for path in base_dir.iterdir() 
                       if path.is_dir()]
        # Файлы не являются папками
        else:
            folders = [path for path in base_dir.iterdir()
                       if path.name[0] != '.']

        return natsorted(folders, key=lambda x: x.name)
    
    @staticmethod
    def get_folder_id(folder):
        return int(folder.name.split()[0])

    @abstractmethod
    def update_child_files(self, child_files):
        pass
            
            
class PhotoUpdater(FileUpdater):

    childs_are_folders = True  # Файлы внутри папок тоже являются папками
    
    def update_child_files(self, child_files):
        
        # Для директории с фото обновляются также подпапки
        self.update(child_files, start_index=1, recursive_update=False)
        
        
class VideoUpdater(FileUpdater):
    
    childs_are_folders = False
    
    def update_child_files(self, child_files):
        pass  # Для видео нет вложенности папок
        


