import asyncio

from re import (
    search as re_search,
)

from ncatbot.core import GroupMessage, PrivateMessage
from ncatbot.plugin import BasePlugin, CompatibleEnrollment

from ncatbot_config import ncatbot_config_dict
from .autoremind_config import AutoRemindYaml


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
        f'AutoRemind需要你提供:\n'
        f'- [任务名],[提醒内容],[提醒时间],[重复次数]\n'
        f'参数格式:'
        f'- /remind add [任务名] "[提醒内容]" "[提醒时间]" [重复次数]\n'
        f'- /remind remove [任务名]\n'
        f'- /remind get [任务名]\n'
        f'提示:\n'
        f'- 该功能仅支持私聊提醒, 请勿使用群组ID\n'
    )
    
    auto_remind_interval_help = (
        '关于解析[提醒时间]参数支持格式:\n'
        '- [一次性任务]:\n'
        '   "YYYY-MM-DD HH:MM:SS"\n'
        '   或 "YYYY:MM:DD-HH:MM:SS"\n'
        '- [每日任务]: "HH:MM"\n'
        '- [间隔任务]:\n'
        '   * 基础单位: "120s", "2h30m", "0.5d"\n'
        '   * 冒号分隔: "00:15:30" (时:分:秒)\n'
        '   * 自然语言: "2天3小时5秒"\n'
        '- [重复次数]:\n'
        '   * 一次性任务必须设置"大于0"的重复次数\n'
        '   * 设置为0次, 意为无次数限制'
    )
    
    def _init_(self) -> None:
        self.auto_remind_yaml = AutoRemindYaml()
        
    async def on_load(self) -> None:
        """
        About why 'event_loop' must be initiallized in 'on_load',
        - BasePlugin:
        >> await asyncio.to_thread(self._init_)
        >> await self.on_load()
        'on_load' function will be called after the new thread eventloop been created.
        
        关于为什么在 'on_load' 函数中初始化 'event_loop':
        - BasePlugin:
        >> await asyncio.to_thread(self._init_)
        >> await self.on_load()
        'on_load'函数会在新线程的事件循环被创建后被调用.
        """
        self.event_loop = asyncio.get_running_loop()
        # Register tasks from 'auto_remind.yaml'
        # 注册'auto_remind.yaml'中的任务
        self.event_loop.create_task(self.register_yaml_task(self.auto_remind_yaml.yaml_task_list))
        
        # Register user tasks from ncatbot internal data persistence file.
        # 注册插件内数据持久化文件内任务
        self.event_loop.create_task(self.data.aload())
        for user_task in self.data.get('user_task', []):
            self.add_scheduled_task(**user_task)
        
    async def on_unload(self) -> None:
        """
        Save others task while the internal yaml tasks from 'jmcomic_config.yaml' had been uninstalled.
        在插件卸载前, 注销 'jmcomic_config.yaml' 配置的任务后, 使用self.data的内置持久化保存其它用户添加的任务
        """
        for name in self.auto_remind_yaml.yaml_task_list:
            self.remove_scheduled_task(name)
        try:
            self.data['user_task'] = self._time_task_scheduler._jobs
            self.data.save()
        # except KeyError:
        #     return None
        finally:
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
            else:
                await msg.reply(text=self.auto_remind_reply)
            return None
        if msg.raw_message.startswith('/remind get'):
            self.event_loop.create_task(self.get_task_status(msg))
            return None
        if msg.raw_message.startswith('/remind add'):
            self.event_loop.create_task(self.user_add_schedule(msg))
            return None
        if msg.raw_message.startswith('/remind remove'):
            self.event_loop.create_task(self.hot_remove_schedule(msg))
            return None
        if msg.raw_message.startswith('/remind reload'):
            self.event_loop.create_task(self.hot_reload_schedule(msg))
            return None
        
        return None
    
    async def register_yaml_task(self, tasks_list: list) -> None:
        """
        Register remind tasks from 'auto_remind.yaml file when current plugin on loading.'
        当前插件加载时, 注册'auto_remind.yaml'中的提醒任务.
        """
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
    
    async def get_task_status(self, msg: GroupMessage | PrivateMessage):
        try:
            name = re_search(r'/remind get "(.+)"', msg.raw_message).group(1)
            status = self._time_task_scheduler.get_job_status(name)
            max_runs = status.get('max_runs')
            text = (
                f'[{status.get('name')}]\n'
                f'计划任务下次运行: {status.get('next_run_time')}\n'
                f'计划任务已执行: {status.get('run_count')}次\n'
                f'计划任务总执行: {max_runs if str(max_runs) + '次' else '无限制'}'
            ) if status else '任务不存在喵'
            await msg.reply(text=text)
        except AttributeError:
            await msg.reply(text='请输入正确的任务名')
        finally:
            return None
    
    async def user_add_schedule(self, msg: GroupMessage | PrivateMessage) -> None:
        """
        Hot add schedule tasks without restart bot.
        热加载计划任务
        """
        try:
            args = re_search(r'/remind add (.+) "(.+)" "(.+)" (.+)', msg.raw_message)
            name, content, interval, max_runs = args.groups()
            max_runs = int(max_runs) if max_runs != '0' else None
            if self.add_scheduled_task(
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
            ):
                await msg.reply(text=f'[{name}]提醒已经添加了喵!将于[{interval}]时提醒您喵')
            else:
                await msg.reply(text=f'[{name}]提醒似乎重复啦喵?')
        except AttributeError:
            await msg.reply(text='参数格式错误,\n详见[/remind help][/remind help -i]')
        except ValueError as v:
            await msg.reply(text=v.args[0])
        finally:
            return None
    
    async def hot_remove_schedule(self, msg: GroupMessage | PrivateMessage) -> None:
        """
        Hot remove schedule tasks without restart bot.
        热卸载计划任务
        """
        name = re_search(r'/remind remove (.+)', msg.raw_message).group(1)
        if self.remove_scheduled_task(name):
            await msg.reply(text=f'提醒[{name}]已删除喵')
        else:
            await msg.reply(text=f'提醒[{name}]不存在或已删除喵')
        return None
    
    async def hot_reload_schedule(self, msg: GroupMessage | PrivateMessage) -> None:
        """
        Hot reload schedule tasks from 'auto_remind.yaml' without restart bot.
        It used class AutoRemindYaml interface to effect
        热重载来自 'auto_remind.yaml' 内配置的计划任务
        使用 'AutoRemindYaml'类 实现
        """
        await msg.reply(text='正在重载中喵')
        for task in self.auto_remind_yaml.yaml_task_list:
            self.remove_scheduled_task(task.get('name'))
        self.auto_remind_yaml.reload_yaml()
        self.event_loop.create_task(self.register_yaml_task(self.auto_remind_yaml.yaml_task_list))
        await msg.reply(text='重载完成喵')
        return None
    
    async def remind_job_func(self, name: str, content: str, group_list: list[str], user_list: list[str]) -> None:
        """
        As job_func callback pass to 'add_scheduled_task()' function.
        传递至 'self.add_scheduled_task()', 作为 'callback' 参数
        """
        text = f'[{name}]: {content}'
        if group_list:
            for group_id in group_list:
                self.event_loop.create_task(self.api.post_group_msg(group_id=group_id, text=text))
        if user_list:
            for user_id in user_list:
                self.event_loop.create_task(self.api.post_private_msg(user_id=user_id, text=text))
            
    @staticmethod
    def remind_job_func_kwargs(yaml_remind_task: dict) -> dict | None:
        try:
            return {
                "name": yaml_remind_task['name'],
                "content": yaml_remind_task['content'],
                "group_list": yaml_remind_task['who_to_remind']['group_id'],
                "user_list": yaml_remind_task['who_to_remind']['user_id'],
            }
        except KeyError:
            return None