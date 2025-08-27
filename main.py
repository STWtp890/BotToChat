from ncatbot.core import BotClient
from ncatbot.utils.config import config
from ncatbot.utils.logger import get_log

import ncatbot_config as ncatbot_config


class NcatBot(BotClient):
    def __init__(self):
        self.read_config(ncatbot_config.attribute_dict)
        super().__init__()
        
        self._ncatbot_logger = get_log("Bot")
    
    @staticmethod
    def read_config(bot_config: dict) -> None:
        config.set_ws_uri(bot_config.get("ws_uri"))        # Set napcat websocket server address
        config.set_token(bot_config.get("token"))          # Set websocket token (napcat ws-server token)
        config.set_webui_uri(bot_config.get("webui_uri"))  # Set webui address
        config.set_bot_uin(bot_config.get("bot_uin"))      # Set bot qq
        config.set_root(bot_config.get("root"))            # Set bot rooter account