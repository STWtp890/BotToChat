from ncatbot.core import BotClient
from ncatbot.utils.config import config
from ncatbot.utils.logger import get_log

import bot_config


# TODO: Here should check if the bot_config.py is exist and init it if not exist.

class NcatBot(BotClient):
	def __init__(self):
		# 设置 bot 配置 (bot_config.py)
		config.set_ws_uri(bot_config.ws_uri)  # 设置 napcat websocket server 地址
		config.set_token(bot_config.token)  # 设置 token (napcat 服务器的 token)
		config.set_webui_uri(bot_config.webui_uri)  # 设置 webui 地址
		config.set_bot_uin(bot_config.bot_uin)  # 设置 bot qq 号 (必填)
		config.set_root(bot_config.root)  # 设置 bot 超级管理员账号 (建议填写)
		
		super().__init__()
		
		_log = get_log("Bot")
