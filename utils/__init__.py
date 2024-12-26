from .database import *
from .helplist import *
from .html_tags import *
from .misc import *
from .strings import *
from .module import *
from .scripts import *
from .modify_pyrogram_client import *
from .getanswer import *
from .filters import *
from .bot_helper import *
from .pastes import *
from .modules import *
from .exceptions import *
from ._logs import *
from config import PREFIX

class Client(ModifyPyrogramClient): ...
class Arg(Argument): ...

from pyrogram.types import Message as M