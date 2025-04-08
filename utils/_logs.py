from datetime import datetime, timedelta
import logging
import os
import re
import tarfile

import coloredlogs

from utils import Config


__all__ = []

if not os.path.exists('logs'):
    os.makedirs('logs')

daily_logs_dir = 'logs/daily_logs'
if not os.path.exists(daily_logs_dir):
    os.makedirs(daily_logs_dir)

run_logs_dir = 'logs/run_logs'
if not os.path.exists(run_logs_dir):
    os.makedirs(run_logs_dir)

general_log_file = 'logs/general.log'
last_run_file = 'logs/last_run.log'

formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s: %(message)s', datefmt='%d-%m-%Y %H:%M:%S')


def get_daily_log_handler():
    today = datetime.now().strftime('%d-%m-%Y')
    daily_log_file = os.path.join(daily_logs_dir, f'day_{today}.log')
    daily_log_handler = logging.FileHandler(daily_log_file, encoding='utf-8', mode='a')
    daily_log_handler.setFormatter(formatter)
    return daily_log_handler


def get_run_log_handler():
    run_log_file = os.path.join(run_logs_dir, 'run_' + datetime.now().strftime('%d-%m-%Y_%H-%M-%S') + '.log')
    run_log_handler = logging.FileHandler(run_log_file, encoding='utf-8', mode='w')
    run_log_handler.setFormatter(formatter)
    return run_log_handler


def get_last_run_log_handler():
    last_run_handler = logging.FileHandler(last_run_file, encoding='utf-8', mode='w')
    last_run_handler.setFormatter(formatter)
    return last_run_handler


def get_general_log_handler():
    general_log_handler = logging.FileHandler(general_log_file, encoding='utf-8', mode='a')
    general_log_handler.setFormatter(formatter)
    return general_log_handler


daily_log_handler = get_daily_log_handler()
run_log_handler = get_run_log_handler()
last_run_handler = get_last_run_log_handler()
general_log_handler = get_general_log_handler()


def install_log(logger, bot=False):
    """
    Устанавливает обработчики логирования и настройки для указанного логгера.

    :param logger: Логгер, для которого нужно установить обработчики.
    :param bot: Флаг, указывающий, использовать ли уровень логирования для бота (BOT_LOGGING_LEVEL).
    :return Logger: Настроенный логгер с добавленными обработчиками.
    """
    logger.setLevel(Config.BOT_LOGGING_LEVEL if bot else Config.LOGGING_LEVEL)
    coloredlogs.install(logger=logger, level=logger.level,
        fmt='%(asctime)s %(name)s %(levelname)s: %(message)s',
        field_styles=dict(
            asctime=dict(color='green'),
            levelname=dict(color='black', bold=True),
            name=dict(color='blue')
        )
    )

    logger.addHandler(general_log_handler)
    logger.addHandler(daily_log_handler)
    logger.addHandler(run_log_handler)
    logger.addHandler(last_run_handler)

    return logger


def auto_delete_old_logs(*, dry_run=False):
    """
    Удаляет старые лог-файлы и архивы .tar.gz по дате в ИМЕНИ файла.
    """
    if not Config.AUTO_DELETE_OLD_LOGFILES:
        return
    
    max_days = Config.DELETE_LOGFILES_OLDER_THAN_DAYS
    cutoff_date = datetime.now() - timedelta(days=max_days)

    # Добавляем обработку .tar.gz
    patterns = [
        (daily_logs_dir, r'day_(\d{2}-\d{2}-\d{4})\.log'),
        (run_logs_dir, r'run_(\d{2}-\d{2}-\d{4})_\d{2}-\d{2}-\d{2}\.log'),
        (daily_logs_dir, r'day_(\d{2}-\d{2}-\d{4})\.tar\.gz'),  # Для .tar.gz
        (run_logs_dir, r'run_(\d{2}-\d{2}-\d{4})_\d{2}-\d{2}-\d{2}\.tar\.gz')  # Для .tar.gz
    ]

    for directory, pattern in patterns:
        for filename in os.listdir(directory):
            match = re.match(pattern, filename)
            if not match:
                continue

            date_str = match.group(1)
            try:
                file_date = datetime.strptime(date_str, '%d-%m-%Y')
            except ValueError:
                continue

            if file_date < cutoff_date:
                file_path = os.path.join(directory, filename)
                try:
                    os.remove(file_path)
                except Exception:
                    pass
    

if Config.AUTO_DELETE_OLD_LOGFILES:
    auto_delete_old_logs(dry_run=True)    


def compress_old_logs():
    """
    Сжимает старые лог-файлы в logs/daily_logs и logs/run_logs в .tar.gz архивы.
    Пропускает текущие активные логи и уже заархивированные файлы.
    """
    current_files = {
        os.path.abspath(get_daily_log_handler().baseFilename),
        os.path.abspath(get_run_log_handler().baseFilename),
        os.path.abspath(get_last_run_log_handler().baseFilename),
        os.path.abspath(get_general_log_handler().baseFilename)
    }

    def compress_dir_logs(directory):
        for filename in os.listdir(directory):
            filepath = os.path.join(directory, filename)
            abspath = os.path.abspath(filepath)

            if not filename.endswith('.log') or abspath in current_files:
                continue

            tar_path = filepath.replace('.log', '.tar.gz')
            if os.path.exists(tar_path):
                continue  # Уже архивирован

            with tarfile.open(tar_path, "w:gz") as tar:
                tar.add(filepath, arcname=os.path.basename(filepath))
            os.remove(filepath)

    compress_dir_logs(daily_logs_dir)
    compress_dir_logs(run_logs_dir)


if Config.COMPRESS_OLD_LOGFILES:
    compress_old_logs()