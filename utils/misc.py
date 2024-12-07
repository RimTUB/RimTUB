from time import perf_counter
from typing import Any

from .helplist import HelpList


__all__ = ['helplist', 'bot_uptime', 'clients', 'groups', 'NCmd']

helplist = HelpList()

bot_uptime = perf_counter()

clients = []

from pyrogram import filters
from config import PREFIX

groups = []


class NCmd:
    group: int
    def __init__(self, client, group, /) -> None:
        self.group = group
        self.client = client
    
    def __call__(self, commands: list) -> Any:
        return self.client.on_message(
            filters.command(commands, PREFIX) & filters.me
            & ~filters.forwarded,
            group=self.group
        )

_objects = {}