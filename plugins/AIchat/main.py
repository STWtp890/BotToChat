from ncatbot.core import GroupMessage, PrivateMessage
from ncatbot.plugin import BasePlugin, CompatibleEnrollment

bot = CompatibleEnrollment


class AIchat(BasePlugin):
    """
    AIchat
    """
    
    name = 'AIchat'
    version = '0.1.0'
    dependencies = {}
    description = 'AIchat'
    
    async def on_load(self) -> None:
        self.add_scheduled_task(
            job_func=self.who_am_i,
            interval='5m',
            name='who_am_i'
        )
    
    async def who_am_i(self):
        login_info = await self.api.get_login_info()
        self.nickname = login_info['data']['nickname']
        self.user_id = login_info['data']['user_id']
    
    @bot.group_event(type='all')
    async def on_group_msg(self, msg: GroupMessage) -> None:
        """
        on_group_msg
        """
        if msg.raw_message.startswith('/'):
            return None
        await self.group_chat_handler(msg)
        return None
    
    @bot.private_event(type='all')
    async def on_private_message(self, msg: PrivateMessage) -> None:
        """
        on_private_message
        """
        if msg.raw_message.startswith('/'):
            return None
        await self.private_chat_handler(msg)
        return None
    
    async def group_chat_handler(self, msg: GroupMessage) -> None:
        """
        group_chat_handler
        """
        # TODO: 1.储存群聊信息
        # TODO: 2.查询摘要与最近n条消息
        # TODO: 3.格式化待输入消息
        # TODO: 4.调用相关函数
        
        pass
    
    async def private_chat_handler(self, msg: PrivateMessage) -> None:
        """
        private_chat_handler
        """
        # TODO: 1.储存私聊信息
        # TODO: 2.查询摘要与最近n条消息
        # TODO: 3.格式化待输入消息
        # TODO: 4.调用相关函数
        
        pass
    
    async def generate_msg(self, msg):
        """
        format the msg to 'openaiful'
        """
        # TODO: 1.格式化待输入消息
        
        pass