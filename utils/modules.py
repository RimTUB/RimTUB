import fnmatch
import zipfile
import shutil
import os

__all__ = [
    'pack_module',
  'unpack_module'
]

def pack_module(module_dir: str, output_filename: int, ignore_file='.rimtubignore') -> str:
    """
    Запаковывает модуль в zip архив

    Создает zip-архив из указанной папки, при этом игнорируя файлы и папки,
    которые соответствуют паттернам из файла ignore_file (по умолчанию '.rimtubignore').

    :param str module_dir: Путь к папке модуля
    :param int output_filename: Имя выходного файла
    :param str ignore_file: Имя файла с паттернами игнорирования, defaults to '.rimtubignore'
    :raises ValueError: Если указанный module_dir не является папкой.
    :return str: Путь к созданному zip-архиву.
    """
    if not os.path.isdir(module_dir):
        raise ValueError(f"{module_dir} не является папкой")

    ignored_patterns = []
    include_patterns = []

    ignore_path = os.path.join(module_dir, ignore_file)
    if os.path.exists(ignore_path):
        with open(ignore_path, 'r', encoding='utf-8') as f:
            for line in f.readlines():
                ignore_item = line.strip()
                if not ignore_item or ignore_item.startswith('#'):
                    continue
                if ignore_item.startswith('!'):
                    include_patterns.append(ignore_item[1:].strip())
                else:
                    ignored_patterns.append(ignore_item)

    def should_ignore(relative_path):
        for pattern in ignored_patterns:
            if fnmatch.fnmatch(relative_path, pattern):
                for include_pattern in include_patterns:
                    if fnmatch.fnmatch(relative_path, include_pattern):
                        return False
                return True
        return False

    with zipfile.ZipFile(output_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(module_dir):
            for file in files:
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, start=module_dir)
                
                if should_ignore(relative_path):
                    continue

                info = zipfile.ZipInfo(relative_path)
                info.date_time = (1980, 1, 1, 0, 0, 0) 

                with open(file_path, 'rb') as f:
                    zipf.writestr(info, f.read())
        
    return output_filename

def unpack_module(input_filename, output_dir):
    if not os.path.isfile(input_filename):
        raise ValueError(f"{input_filename} не найден")

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with zipfile.ZipFile(input_filename, 'r') as zipf:
        for member in zipf.namelist():
            member_path = os.path.join(output_dir, member) 
            
            if member.endswith('/'):
                os.makedirs(member_path, exist_ok=True)
            else:
                os.makedirs(os.path.dirname(member_path), exist_ok=True)
                with zipf.open(member) as source_file:
                    with open(member_path, 'wb') as target_file:
                        shutil.copyfileobj(source_file, target_file)
    
    return output_dir



