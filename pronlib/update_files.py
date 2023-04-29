import re
from abc import ABC, abstractmethod

from natsort import natsorted


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
        self.main_folders = self.get_files(base_dir)
        self.start_index = start_index
    
    def update(self, folders=None, start_index=None, recursive_update=True):
        
        if folders is None:
            folders = self.main_folders

        if start_index is None:
            start_index = self.start_index
        
        temp_folders = []
            
        for cur_id, folder in enumerate(folders, start=start_index):
            name_components = folder.name.split()

            # Если у папки нет индекса
            if re.match(r'\d+$', name_components[0]) is None:
                name_components.insert(0, str(cur_id))

            # Изменение индекса
            if name_components[0] != str(cur_id):
                name_components[0] = str(cur_id)

            # Обновление подпапок
            if recursive_update:
                child_files = self.get_files(folder)
                self.update_child_files(child_files)
                self.change_total(name_components, child_files)

            new_name = ' '.join(name_components)
            # Сначала переименовываем в "новое имя_", потом в "новое имя"
            # чтобы избежать конфликтов, когда файл "новое имя" уже есть
            temp_folders.append(folder.rename(folder.parent / (new_name+'_')))

        for folder in temp_folders:
            folder.rename(folder.parent / folder.name[:-1])

    @staticmethod
    def change_total(name_components, child_files):
        '''
        Изменяет/добавляет последнюю строку в списке name_components, обозначающей колво файлов внутри папки (child_files - файлы папки)
        '''
        
        amount_of_files = len(child_files)
        new_total_str = f'({amount_of_files})'
        
        if re.match(r'\(.+\)', name_components[-1]):
            name_components[-1] = new_total_str
        else:
            name_components.append(new_total_str)
            
    def get_files(self, base_dir=None, childs_are_folders=None):
        '''
        Получить список файлов в директории
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
        


