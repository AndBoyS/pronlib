import re


class FileUpdater:
    '''
    Обновляет индексы и счетчики в названиях папок
    '''
    def __init__(self, base_dir):
        self.base_dir = base_dir
        self.main_folders = self.get_files(base_dir)
    
    def update(self, folders=None, start_index=None, update_total=True):
        
        if folders is None:
            folders = self.main_folders
        if start_index is None:
            start_index = self.start_index
        cur_id = start_index
        
        temp_folders = []
            
        for folder in folders:
            name_components = folder.name.split()
        
            if name_components[0] != str(cur_id):
                name_components[0] = str(cur_id)
                
            if update_total:
                child_files = self.get_files(folder, numbered_folders=self.childs_are_folders)
                self.update_child_files(child_files)
                self.change_total(name_components, child_files)
                
            new_name = ' '.join(name_components)
            # Сначала переименовываем в "новое имя_", потом в "новое имя"
            # чтобы избежать конфликтов, когда файл "новое имя" уже есть
            temp_folders.append(folder.rename(folder.parent / (new_name+'_')))
    
            cur_id += 1
            
        [folder.rename(folder.parent / folder.name[:-1]) 
         for folder in temp_folders]
        
    def change_total(self, name_components, child_files):
        '''
        Изменяет/добавляет последнюю строку в списке name_components, обозначающей колво файлов внутри папки (child_files - файлы папки)
        '''
        
        amount_of_files = len(child_files)
        new_total_str = f'({amount_of_files})'
        
        if re.match(r'\(.+\)', name_components[-1]):
            name_components[-1] = new_total_str
        else:
            name_components.append(new_total_str)
            
    def get_files(self, base_dir=None, numbered_folders=True):
        '''
        Получить список файлов в директории, при numbered_folders=True, файлы являются папками с индексами в названии
        '''
        if base_dir is None:
            base_dir = self.base_dir
            
        if numbered_folders:
            folders = [path for path in base_dir.iterdir() 
                       if path.is_dir() and path.name[0].isdigit()]
            return sorted(folders, key=self.get_folder_id)
        
        else:
            return [path for path in base_dir.iterdir() 
                    if path.name[0] != '.']
    
    @staticmethod
    def get_folder_id(folder):
        return int(folder.name.split()[0])
            
            
class PhotoUpdater(FileUpdater):
    
    start_index = 0  # Нумерация папок начинается с нуля
    childs_are_folders = True  # Файлы внутри папок тоже являются папками
    
    def update_child_files(self, child_files):
        
        # Для директории с фото обновляются также подпапки
        self.update(child_files, start_index=1, update_total=False)
        
        
class VideoUpdater(FileUpdater):
    
    childs_are_folders = False
    
    def __init__(self, base_dir, photos_dir):
        super().__init__(base_dir)
        self.start_index = len(self.get_files(photos_dir))
        
    def update_child_files(self, child_files):
        pass
        


