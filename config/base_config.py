# НЕ ТРОЖЬ ЕСЛИ НЕ ЗНАЕШЬ ЧТО ЭТО !!!

API_ID = 22983860
API_HASH = "37c11863c1bf2330c0cc64d1755f9e60"

DATABASE_FILE = 'database.db'

import logging
LOGGING_LEVEL = logging.DEBUG
BOT_LOGGING_LEVEL = logging.DEBUG


DMF_TIMEOUT = 5
DML_TIMEOUT = 5

CHECK_HASH_URL = "https://rimtub.pp.ua/check/{hash}"
DML_WHITELIST  = ['rimtub.pp.ua']


PROXY = None
CL_DEVICE_MODEL = 'M2102J20SG'
CL_SYSTEM_VERSION = 'SDK 30'
CL_LANG_PACK = 'android'
CL_LANG_CODE = 'ru'
CL_SYSTEM_LANG_CODE = 'ru_RU'

from pyrogram.enums import ClientPlatform
CL_CLIENT_PLATFORM = ClientPlatform.WEB