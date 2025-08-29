from os import path
from re import search

import yaml
import asyncio

from ncatbot.core import GroupMessage, PrivateMessage
from ncatbot.plugin import BasePlugin
from ncatbot.plugin import CompatibleEnrollment

from .jmcomic_handler import JMcomicHandler
from .jmcomic_path import jmcomic_base_dir

# read jmcomic config yaml
class ReplyTextYaml:
    def __init__(self):
        self.__yaml_path = path.join(jmcomic_base_dir, "jmcomic_reply.yaml")
        if not self._config_exist():
            self._new_config_yaml()
        self._set_config()
        
    def _config_exist(self) -> bool:
        return path.exists(f"{self.__yaml_path}")
    
    def _new_config_yaml(self) -> None:
        with open(f"{self.__yaml_path}", "w") as cfg:
            cfg.write(
                f'text_help: "输入:/jm [神秘数字], 来获取漫画, 等待下载后漫画就会发送喵" \n'
                f'text_before_send_comic: "稍等喵, 漫画正在处理中..." \n'
            )
            
    def _set_config(self):
        _yaml_attribute = self._get_yaml()
        # config
        self.text_help = _yaml_attribute["text_help"]
        self.text_before_send_comic = _yaml_attribute["text_before_send_comic"]
        
    def _get_yaml(self) -> dict:
        return yaml.load(open(self.__yaml_path, "r", encoding="utf-8"), Loader=yaml.FullLoader)

reply_text_yaml = ReplyTextYaml()
text_attribute_dict = {
    "text_help": reply_text_yaml.text_help,
    "text_before_send_comic": reply_text_yaml.text_before_send_comic,
}


bot = CompatibleEnrollment

class JMComic(BasePlugin):
    """
    - By using jmcomic API to get the comic.
    - As a message reactor
    - As a task producer
        - provide a comic download task
    - As a file sender
        - find the download file and post
    """

    name = 'JMComic'
    version = '1.0.0'
    dependencies = {}
    description = 'JMComic'

    async def on_load(self):
        self.loop = asyncio.get_event_loop()
        self.jmcomic = JMcomicHandler()

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
            await msg.reply(text=text_attribute_dict["text_help"])
            return None

        try:
            album_id = search(r'/jm (\d+)', msg.raw_message).group(1)
        except AttributeError:
            await msg.reply(text="没有数字你在逗我喵?")
            return None

        await self.post_message(msg, text=text_attribute_dict["text_before_send_comic"])
        await self.send_comic(msg, album_id)

        return None
        
    async def send_comic(self, msg: GroupMessage | PrivateMessage, album_id: str) -> None:
        
        if not album_id:
            await self.post_message(msg, "没有数字你在逗我喵?")
            
        album: dict | None = await self.jmcomic.find(album_id)
        if not album:
            await self.post_message(msg, "漫画下载出了点问题喵")

        await self.post_file(msg, file_path=album["pdf_file_path"])
        await self.post_message(msg, text=f'名为\n"{album["album_name"]}"\n的漫画已经发送啦喵')
        
    async def post_message(self, msg: GroupMessage | PrivateMessage, text: str) -> None:
        """
        Pack post method, check msg type and use different method.

        :param msg: The incoming message object, can be either a group message or a private message.
        :param text: As param for post method.
        """
        if isinstance(msg, GroupMessage):
            await self.api.post_group_msg(msg.group_id, text=text)
        elif isinstance(msg, PrivateMessage):
            await self.api.post_private_msg(msg.user_id, text=text)
        else:
            raise TypeError
    
    async def post_file(self, msg: GroupMessage | PrivateMessage, file_path: str) -> None:
        """
        Pack post method, check msg type and use different method.

        :param msg: The incoming message object, can be either a group message or a private message.
        :param file_path: As param for post method.
        """
        if isinstance(msg, GroupMessage):
            await self.api.post_group_file(msg.group_id, file=file_path)
        elif isinstance(msg, PrivateMessage):
            await self.api.post_private_file(msg.user_id, file=file_path)
        else:
            raise TypeError