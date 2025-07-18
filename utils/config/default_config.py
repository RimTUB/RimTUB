from typing import List
import logging
from pyrogram.enums import ClientPlatform


class DefaultConfig:

    VERSION = '2.2.2-5'
    VERSION_TUPLE = (2, 2, 2, 'release', 5)


    PHONES: List[str]
    BOT_TOKEN: str
    PREFIX: str = "."
    PLAY_SOUND: bool = False
    SHOW_NOTIFICATION: bool = True
    SHOW_HEADER_IN_HELP: bool = True
    SHOW_MODULES_WITH_COMMAND_IN_HELP: bool = True


    API_ID: int|str = 22983860
    API_HASH: str = "37c11863c1bf2330c0cc64d1755f9e60"

    LOGGING_LEVEL: int = logging.DEBUG
    BOT_LOGGING_LEVEL: int = logging.ERROR
    DEFAULT_MODULE_LOGGING_LEVEL: int = logging.DEBUG

    DISABLE_STARTUP_MESSAGE: bool = False

    DMF_TIMEOUT: int|float = 5
    DML_TIMEOUT: int|float = 5

    CHECK_HASH_URL: str = "https://rimtub.pp.ua/api/checkHash/{hash}"
    DML_WHITELIST: List[str] = ['rimtub.pp.ua']

    DISABLE_MODULE_CHECKING: bool = False
    DISABLE_MODULE_VERSION_CHECKING: bool = False

    CHECK_VERSIONS_URL: str = "https://rimtub.pp.ua/api/getAvaiableRimTUBModuleVersions/{module_name}/{module_version}"

    PROXY: dict = None
    CL_DEVICE_MODEL: str = 'M2102J20SG'
    CL_SYSTEM_VERSION: str = 'SDK 30'
    CL_LANG_PACK: str = 'android'
    CL_LANG_CODE: str = 'ru'
    CL_SYSTEM_LANG_CODE: str = 'ru_RU'

    CL_CLIENT_PLATFORM: ClientPlatform = ClientPlatform.OTHER


    
    PICKLE_STORAGE_META_FILE = 'pickle_meta.json'
    CLEANUP_EXPIRED_PICKLE_STORAGE_FILES_INTERVAL = 3600
    DEFAULT_PICKLE_STORAGE_FILES_TTL = 3600*24*3
    
    
    COMPRESS_OLD_LOGFILES = True
    AUTO_DELETE_OLD_LOGFILES = True
    DELETE_LOGFILES_OLDER_THAN_DAYS = 7
