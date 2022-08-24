import re
import json
from pathlib import Path
from natsort import natsorted

# 69 Aboba (5)
folder_name_pattern = re.compile(r'\d+ (.+) \(\d+\)')
# 69 Aboba
subfolder_name_pattern = re.compile(r'\d+ (.+)')


def get_subfolders(folder: Path):
    return natsorted([path for path in folder.glob('*') if path.is_dir()], 
                     key=lambda x: x.name)


def update_meta_files(base_folder: Path, summary_path='summary.txt'):
    '''
    Создает/обновляет файлы meta.json в подпапках (таргет: Photos)
    '''
    folders = get_subfolders(base_folder)
    
    summary = ''

    for folder in folders:
        if 'Archive' in folder.name or not re.match(r'\d', folder.name):
            continue

        subfolders = get_subfolders(folder)
        # Есть ли папки без названий (для них в meta для атрибута name используется название папки-родителя)
        does_have_blank_names = any(re.match(r'\d+$', path.name) for path in subfolders)
        if does_have_blank_names:
            get_set_meta_data(folder, folder_name_pattern)

        summary += ' '.join([folder.name, '\n'])

        for subfolder in subfolders:

            subfolder_name = subfolder.name

            if not re.match(r'\d+$', subfolder_name):
                name, artist = get_set_meta_data(subfolder, subfolder_name_pattern)
                if name:
                    summary += '\t' + ' '.join([name, '-', artist, '\n'])

    with open(base_folder / summary_path, 'w') as f:
        f.write(summary)


def load_json(fp: Path):
    with open(fp, 'r') as f:
        return json.load(f)


def dump_json(obj, fp: Path):
    with open(fp, 'w') as f:
        json.dump(obj, f)


def get_set_meta_data(folder: Path, re_pattern) -> (str, str):
    '''
    Получить мета данные из folder / 'meta.json' + создать meta.json если он отсутствует
    '''
    folder_name = folder.name
    folder_name_match = re_pattern.search(folder_name)
    if folder_name_match is None:
        return '', ''
    folder_name = folder_name_match.group(1)

    # Если файла meta.json нет в подпапке
    if not list(folder.glob('meta.json')):

        meta_artist = extract_artist_from_folder_name(folder_name)

        meta_data = {'name': folder_name,
                     'artist': meta_artist}

        dump_json(meta_data, folder / 'meta.json')
        meta_name = folder_name

    # Если файл meta.json существует
    else:
        meta_data = load_json(folder / 'meta.json')

        # Если не указан художник, попробовать чекнуть название папки
        # и обновить метадату
        if not meta_data['artist']:
            meta_data['artist'] = extract_artist_from_folder_name(folder_name)
            if meta_data['artist']:
                dump_json(meta_data, folder / 'meta.json')

        meta_name = meta_data['name']
        meta_artist = meta_data['artist']

    return meta_name, meta_artist


def extract_artist_from_folder_name(folder_name: str):
    # Имя автора может находится в названии папки
    # пример: big booba doujinshi [artist name]
    meta_artist_match = re.search(r'\[(.+)\]', folder_name)
    if meta_artist_match is None:
        return ''
    else:
        return meta_artist_match.group(1)


def update_random_file(photos_dir, videos_dir, file_path='sauce.json'):
    folders = list(photos_dir.glob('*')) + list(videos_dir.glob('*'))
    folder_to_random = {}
    for folder in folders:
        if 'Archive' in folder.name:
            continue

        name = folder.name
        # В первой скобке название категории, во второй - число
        category_match = re.search(r'(.+) \((\d+)\)', name)
        if category_match is None:
            continue

        category_name = category_match.group(1)
        category_number = int(category_match.group(2))
        folder_to_random[category_name] = category_number

    with open(file_path, 'w') as f:
        json.dump(folder_to_random, f)
