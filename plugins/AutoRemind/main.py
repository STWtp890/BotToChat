import asyncio

from re import (
    search as re_search,
)

from ncatbot.core import GroupMessage, PrivateMessage
from ncatbot.plugin import BasePlugin, CompatibleEnrollment

from .auto_remind_yaml import AutoRemindYaml


bot = CompatibleEnrollment

class AutoRemind(BasePlugin):
    """
    AutoRemind
    """

    name = 'AutoRemind'
    version = '1.0.0'
    dependencies = {}
    description = 'AutoRemind'
    
    auto_remind_reply = (
        f'AutoRemindHelp需要你提供\n'
        f'- [任务名], [提醒内容], [提醒时间], [最多重复次数]\n'
        f'/remind add [任务名] [提醒内容] [提醒时间] [最多重复次数]\n'
        f'/remind remove [任务名]'
    )
    
    auto_remind_interval_help = (
        '解析时间参数支持格式:\n'
        '- 一次性任务:\n'
        '   "YYYY-MM-DD HH:MM:SS"\n'
        '   或 "YYYY:MM:DD-HH:MM:SS"\n'
        '- 每日任务: "HH:MM"\n'
        '- 间隔任务:\n'
        '   * 基础单位: "120s", "2h30m", "0.5d"\n'
        '   * 冒号分隔: "00:15:30" (时:分:秒)\n'
        '   * 自然语言: "2天3小时5秒"'
    )
    
    def _init_(self) -> None:
        self.auto_remind_yaml = AutoRemindYaml()
        
    async def on_load(self) -> None:
        self.event_loop = asyncio.get_event_loop()
        
        await self.yaml_register_schedule(self.auto_remind_yaml.task_list)
        for user_task in self.data.get('user_task', []):
            self.add_scheduled_task(**user_task)
        
    async def on_unload(self) -> None:
        """ Save user tasks and uninstall the internal tasks when plugin unload """
        for name in self.auto_remind_yaml.task_list:
            self.remove_scheduled_task(name)
        try:
            self.data['user_task'] = self._time_task_scheduler._jobs
        except KeyError:
            return None
    
    @bot.group_event(types='all')
    async def on_group_msg(self, msg: GroupMessage):
        self.event_loop.create_task(self.on_msg(msg))
    
    @bot.private_event(types='all')
    async def on_private_message(self, msg: PrivateMessage):
        self.event_loop.create_task(self.on_msg(msg))
        
    async def on_msg(self, msg: GroupMessage | PrivateMessage) -> None:
        if not msg.raw_message.startswith('/remind'):
            return None
        if msg.raw_message.startswith('/remind help'):
            if msg.raw_message.find('-i'):
                await msg.reply(text=self.auto_remind_interval_help)
            await msg.reply(text=self.auto_remind_reply)
            return None
        if msg.raw_message.startswith('/remind add'):
            await self.hot_add_schedule(msg)
            return None
        if msg.raw_message.startswith('/remind remove'):
            name = re_search(r'/remind remove (.+)', msg.raw_message).group(1)
            self.remove_scheduled_task(name)
            return None
        if msg.raw_message.startswith('/remind reload'):
            await self.hot_reload_schedule()
            return None
        
        return None
    
    async def yaml_register_schedule(self, tasks_list: list) -> None:
        for task in tasks_list:
            if not task.get('enable'):
                continue
                
            self.add_scheduled_task(
                name=task.get('name'),
                job_func=self.remind_job_func,
                interval=task.get('interval'),
                max_runs=None,
                kwargs=self.remind_job_func_kwargs(task),
            )
            
    @staticmethod
    def remind_job_func_kwargs(task: dict) -> dict | None:
        try:
            return {
                "content": task['content'],
                "group_id": task['who_to_remind']['group_id'],
                "user_id": task['who_to_remind']['user_id'],
            }
        except KeyError:
            return None
        
    async def hot_add_schedule(self, msg: GroupMessage | PrivateMessage) -> None:
        """ Hot add schedule tasks witout restart bot. """
        try:
            args = re_search(r'/remind add (.+) (.+) (.+) (.+)', msg.raw_message)
        except AttributeError:
            await msg.reply(text='参数格式错误,\n详见[/remind help][/remind help -i]')
            return None
        
        name, content, interval, max_runs = args.groups()
        try:
            self.add_scheduled_task(
                name=name,
                job_func=self.remind_job_func,
                interval=interval,
                max_runs=max_runs,
                kwargs={
                    'name': name,
                    'content': content,
                    'group_id': [],
                    'user_id': [msg.user_id, ]
                },
            )
        except ValueError as v:
            await msg.reply(text=v.args[0])
            
        return None
    
    async def hot_reload_schedule(self) -> None:
        """ Hot reload schedule tasks witout restart bot. """
        for name in self.auto_remind_yaml.task_list:
            self.remove_scheduled_task(name)
        self.auto_remind_yaml.reload_yaml()
        await self.yaml_register_schedule(self.auto_remind_yaml.task_list)
    
    async def remind_job_func(self, name: str, content: str, group_id: list, user_id: list) -> None:
        """ As job_func call by 'add_scheduled_task()' function. """
        text = f'[{name}]: {content}'
        for id in group_id:
            await self.api.post_group_msg(group_id=id, text=text)
        for id in user_id:
            await self.api.post_private_msg(user_id=id, text=text)
        