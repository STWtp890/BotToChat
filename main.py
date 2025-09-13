from ncatbot.core import BotClient
from ncatbot.utils.logger import get_log


class NcatBot(BotClient):
    def __init__(self):
        super().__init__()
        self._ncatbot_logger = get_log("Bot")