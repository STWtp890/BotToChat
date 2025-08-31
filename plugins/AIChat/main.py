import asyncio

from ncatbot.core import GroupMessage, PrivateMessage
from ncatbot.plugin import BasePlugin, CompatibleEnrollment


bot = CompatibleEnrollment

class AIChat(BasePlugin):
    name = 'AIChat'
    version = '1.0.0'
    dependencies = {}
    description = 'AIChat'

    async def on_load(self):
        self.loop = asyncio.get_event_loop()

    @bot.group_event(types='all')
    async def on_group_msg(self, msg: GroupMessage):
        self.loop.create_task(self.on_msg(msg))

    @bot.private_event(types='all')
    async def on_private_message(self, msg: PrivateMessage):
        self.loop.create_task(self.on_msg(msg))
    
    async def on_msg(self, msg: GroupMessage | PrivateMessage) -> None:
        pass