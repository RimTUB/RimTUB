from .config import Config
from .database import *
from .html_tags import *
from .scripts import *
from .misc import *
from .strings import *
from .module import *
from .modify_pyrogram_client import *
from .filters import *
from .bot_helper import *
from .pastes import *
from .modules import *
from .exceptions import *
from ._logs import *

class Client(ModifyPyrogramClient): ...

from pyrogram.types import Message as M
