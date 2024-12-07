from datetime import datetime
import logging
import os

import coloredlogs

from config.base_config import BOT_LOGGING_LEVEL, LOGGING_LEVEL

__all__ = [
    'install_log'
]

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
    logger.setLevel(BOT_LOGGING_LEVEL if bot else LOGGING_LEVEL)
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