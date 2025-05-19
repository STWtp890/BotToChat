import asyncio
from re import search

from ncatbot.core import GroupMessage, PrivateMessage
from ncatbot.plugin import BasePlugin
from ncatbot.plugin import CompatibleEnrollment

from .comic_handler.comic_handler import JMcomicHandler


text_before_send = '稍等喵, 漫画正在处理中...'

text_help = (
    '输入 "/jm [神秘数字]" 来获取漫画\n'
    '等待下载后, 漫画会发送到你的私聊喵'
)

text_without_album = '数字都没有, 你在逗我喵?'

def check_jmcfg() -> bool:
    """
    Check if jmcomic_config.py exists
    """
    from os.path import exists
    return exists("./jmcomic_config.py")
def new_jmcfg() -> None:
    """
    New a jmcomic_config file for jmoption
    """
    with open("./jmcomic_config.py", "w") as cfg:
        cfg.write(
            "jmcomic_username = ''\n"
            "jmcomic_password = ''\n"
        )


bot = CompatibleEnrollment

class JMcomic(BasePlugin):
    """
    - By using jmcomic API to get the comic.
    - It needs to be added as a friend before using to avoid being blocked.
    """

    name = 'JMcomic'
    version = '1.0.0'
    dependencies = {}
    description = 'Get JMcomic'

    async def on_load(self):
        if not check_jmcfg():
            new_jmcfg()
            
        self.loop = asyncio.get_event_loop()
        self.jmcomic = JMcomicHandler(self.api)

    @bot.group_event(types='all')
    async def on_group_msg(self, msg: GroupMessage):
        self.loop.create_task(self.on_msg(msg))

    @bot.private_event(types='all')
    async def on_private_message(self, msg: PrivateMessage):
        self.loop.create_task(self.on_msg(msg))

    async def on_msg(self, msg: GroupMessage | PrivateMessage) -> None:
        """
        Handles incoming messages to process commands starting with '/jm'.
        
        :param msg: The incoming message object, can be either a group message or a private message.
        """
        if not msg.raw_message.startswith('/jm'):
            return None

        if msg.raw_message.startswith('/jm help'):
            await msg.reply(text=text_help)
            return None

        # # Capture and check the album_id.
        album_id = search(r'/jm (\d+)', msg.raw_message).group(1)
        if not album_id:
            await msg.reply(text=text_without_album)
            return None

        # Add task to events loop.
        self.loop.create_task(self._post_msg(msg))
        self.loop.create_task(self.jmcomic.handler(album_id=album_id, msg=msg))
        return None
    
    async def _post_msg(self, msg: GroupMessage | PrivateMessage) -> None:
        """
        Pack post method, check msg type and use different method.
        
        :param msg: The incoming message object, can be either a group message or a private message.
        """
        if isinstance(msg, GroupMessage):
            await self.api.post_group_msg(msg.group_id, text=text_before_send)
        elif isinstance(msg, PrivateMessage):
            await self.api.post_private_msg(msg.user_id, text=text_before_send)
        else:
            raise TypeError('msg is not GroupMessage or PrivateMessage')