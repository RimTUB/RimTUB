from datetime import datetime, timedelta
import logging
import re
import tarfile
from pathlib import Path

import coloredlogs

from utils import Config

__all__ = []

logs_dir = Path('logs')
logs_dir.mkdir(exist_ok=True)

daily_logs_dir = logs_dir / 'daily_logs'
daily_logs_dir.mkdir(exist_ok=True)

run_logs_dir = logs_dir / 'run_logs'
run_logs_dir.mkdir(exist_ok=True)

last_run_file = logs_dir / 'last_run.log'

formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s: %(message)s', datefmt='%d-%m-%Y %H:%M:%S')

logger = logging.getLogger('RimTUB')

def get_daily_log_handler():
    today = datetime.now().strftime('%d-%m-%Y')
    daily_log_file = daily_logs_dir / f'day_{today}.log'
    handler = logging.FileHandler(daily_log_file, encoding='utf-8', mode='a')
    handler.setFormatter(formatter)
    return handler


def get_run_log_handler():
    timestamp = datetime.now().strftime('%d-%m-%Y_%H-%M-%S')
    run_log_file = run_logs_dir / f'run_{timestamp}.log'
    handler = logging.FileHandler(run_log_file, encoding='utf-8', mode='w')
    handler.setFormatter(formatter)
    return handler


def get_last_run_log_handler():
    handler = logging.FileHandler(last_run_file, encoding='utf-8', mode='w')
    handler.setFormatter(formatter)
    return handler


daily_log_handler = get_daily_log_handler()
run_log_handler   = get_run_log_handler()
last_run_handler  = get_last_run_log_handler()


def install_log(logger, bot=False):
    """
    Устанавливает обработчики логирования и настройки для указанного логгера.
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

    logger.addHandler(daily_log_handler)
    logger.addHandler(run_log_handler)
    logger.addHandler(last_run_handler)

    return logger


def auto_delete_old_logs():
    """
    Удаляет старые лог-файлы и архивы .tar.gz по дате в ИМЕНИ файла.
    """
    if not Config.AUTO_DELETE_OLD_LOGFILES:
        return

    max_days = Config.DELETE_LOGFILES_OLDER_THAN_DAYS
    cutoff_date = datetime.now() - timedelta(days=max_days)

    patterns = [
        (daily_logs_dir, r'day_(\d{2}-\d{2}-\d{4})\.log'),
        (run_logs_dir, r'run_(\d{2}-\d{2}-\d{4})_\d{2}-\d{2}-\d{2}\.log'),
        (daily_logs_dir, r'day_(\d{2}-\d{2}-\d{4})\.tar\.gz'),
        (run_logs_dir, r'run_(\d{2}-\d{2}-\d{4})_\d{2}-\d{2}-\d{2}\.tar\.gz')
    ]

    for directory, pattern in patterns:
        for path in directory.iterdir():
            try:
                match = re.match(pattern, path.name)
                if not match:
                    continue

                try:
                    file_date = datetime.strptime(match.group(1), '%d-%m-%Y')
                except ValueError:
                    continue

                if file_date < cutoff_date:
                        path.unlink()
            except:
                logger.warning(f'Can\' delete log {path}. Traceback on debug level')
                logger.debug('.', exc_info=True)


if Config.AUTO_DELETE_OLD_LOGFILES:
    auto_delete_old_logs()


def compress_old_logs():
    """
    Сжимает старые лог-файлы в logs/daily_logs и logs/run_logs в .tar.gz архивы.
    Пропускает текущие активные логи и уже заархивированные файлы.
    """
    current_files = {
        Path(get_daily_log_handler().baseFilename).resolve(),
        Path(get_run_log_handler().baseFilename).resolve(),
        Path(get_last_run_log_handler().baseFilename).resolve(),
    }

    def compress_dir_logs(directory: Path):
        for path in directory.iterdir():
            try:
                if not path.name.endswith('.log') or path.resolve() in current_files:
                    continue

                tar_path = path.with_suffix('.tar.gz')
                if tar_path.exists():
                    continue

                with tarfile.open(tar_path, "w:gz") as tar:
                    tar.add(path, arcname=path.name)
                    
                path.unlink()
            except:
                logger.warning(f'Can\' compress log {path}. Traceback on debug level')
                logger.debug('.', exc_info=True)

    compress_dir_logs(daily_logs_dir)
    compress_dir_logs(run_logs_dir)


if Config.COMPRESS_OLD_LOGFILES:
    compress_old_logs()
