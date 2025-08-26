from ncatbot.core import BotClient
from ncatbot.utils.config import config
from ncatbot.utils.logger import get_log


class NcatBot(BotClient):
    def __init__(self):
        import ncatbot_config as ncbt
        self.read_config(ncbt.config)
        super().__init__()
        
        _log = get_log("Bot")
    
    @staticmethod
    def read_config(bot_config: dict) -> None:
        config.set_ws_uri(bot_config["ws_uri"])        # Set napcat websocket server addr
        config.set_token(bot_config["token"])          # Set websocket token (napcat wsserver token)
        config.set_webui_uri(bot_config["webui_uri"])  # Set webui addr
        config.set_bot_uin(bot_config["bot_uin"])      # Set bot qq
        config.set_root(bot_config["root"])            # Set bot rooter account