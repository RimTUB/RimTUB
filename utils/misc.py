from time import perf_counter
from typing import Any

from .helplist import HelpList


__all__ = ['helplist', 'bot_uptime', 'clients', 'groups', 'NCmd', 'get_module_name_by_group']

helplist = HelpList()

bot_uptime = perf_counter()

clients = []

from pyrogram import filters
from config import PREFIX

groups = []

def get_module_name_by_group(group, module_groups):
    for module_name, groups in module_groups.items():
        if group in groups:
            return module_name
    return None


class NCmd:
    group: int
    def __init__(self, client, group, /) -> None:
        self.group = group
        self.client = client
    
    def __call__(self, commands: list) -> Any:
        def wrapper(func):
            @self.client.on_message(
                filters.command(commands, prefixes=[PREFIX, PREFIX+' ']) & filters.me
                & ~filters.forwarded,
                group=self.group
            )
            async def __wrapper(client, message):
                try:
                    await func(client, message)
                except:
                    client.logger.error(f"Error in command {message.command[0]} "
                                     f"(module {get_module_name_by_group(self.group, client._module_groups)})",
                                     exc_info=True)
        return wrapper

_objects = {}