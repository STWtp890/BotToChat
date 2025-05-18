from ncatbot.core import BotClient
from ncatbot.utils.config import config
from ncatbot.utils.logger import get_log


class NcatBot(BotClient):
    def __init__(self):
        if not self.config_exist:
            self.new_config()
            
        import bot_config
        self.read_config()
        super().__init__()
        
        _log = get_log("Bot")
    
    @staticmethod
    def read_config() -> None:
        config.set_ws_uri(bot_config.ws_uri)        # Set napcat websocket server addr
        config.set_token(bot_config.token)          # Set websocket token (napcat wsserver token)
        config.set_webui_uri(bot_config.webui_uri)  # Set webui addr
        config.set_bot_uin(bot_config.bot_uin)      # Set bot qq
        config.set_root(bot_config.root)            # Set bot rooter account
    
    @staticmethod
    def new_config() -> None:
        with open("bot_config.py", "w") as cfg:
            cfg.write(
                f"# ncatbot config"
                f"ws_uri = \"ws://localhost:3001\"      # websocket uri\n"
                f"token = \"\"                          # ws token\n"
                f"webui_uri = \"http://localhost:6099\" # napcat webui\n"
                f"bot_uin = \"\"                        # bot uin\n"
                f"root = \"\"                           # rooter\n"
            )
    
    @staticmethod
    def config_exist() -> bool:
        from os.path import exists
        return exists("bot_config.py")