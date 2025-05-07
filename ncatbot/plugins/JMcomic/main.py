import asyncio
from re import search

from ncatbot.core import GroupMessage, PrivateMessage
from ncatbot.plugin import BasePlugin
from ncatbot.plugin import CompatibleEnrollment

from .jmcomic_handler import JMcomicHandler

bot = CompatibleEnrollment


class JMcomic(BasePlugin):
	"""
	- By using jmcomic API to get the comic.
	- It needs to be added as a friend before using to avoid being blocked.
	"""
	
	name = 'JMcomic'
	version = '0.1.0'
	dependencies = {}
	description = 'Get JMcomic'
	
	async def on_load(self):
		self.loop = asyncio.get_event_loop()
		self.jmcomic = JMcomicHandler(self.api)
	
	@bot.group_event(types='all')
	async def on_group_msg(self, msg: GroupMessage):
		self.loop.create_task(self.on_msg(msg))
	
	@bot.private_event(types='all')
	async def on_private_message(self, msg: PrivateMessage):
		self.loop.create_task(self.on_msg(msg))
	
	async def on_msg(self, msg: GroupMessage | PrivateMessage) -> None:
		if not msg.raw_message.startswith('/jm'):
			return None
		
		if msg.raw_message.startswith('/jm help'):
			await self.help(msg)
			return None
		
		# 获取并检测漫画ID合法性
		album_id = search(r'\d+', msg.raw_message)
		if album_id is None:
			await msg.reply(text='数字都没有, 你在逗我喵?')
			return None
		
		album_id = album_id[0]
		
		# 下载任务添加至事件循环
		self.loop.create_task(self.api.post_group_msg(msg.group_id, text='稍等喵, 漫画正在处理中...'))
		self.loop.create_task(self.jmcomic.handler(album_id=album_id, msg=msg))
		return None
	
	@staticmethod
	async def help(msg: GroupMessage):
		await msg.reply(
			text=(
				f'使用jm指令前, 记得添加我好友喵~\n'
				f'输入 \"/jm [神秘数字]\" 来获取漫画\n'
				f'等待下载后, 漫画会发送到你的私聊喵'
			)
		)
