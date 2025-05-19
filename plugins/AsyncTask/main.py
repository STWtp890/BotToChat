import asyncio

from ncatbot.plugin import BasePlugin, CompatibleEnrollment


bot = CompatibleEnrollment

class AsyncTask(BasePlugin):
    """
    AsyncTask
    """

    name = 'AsyncTask'
    version = '1.0.0'
    dependencies = {}
    description = 'AsyncTask'
    
    async def on_load(self):
        """
        on_load
        """
        await self.update_list()
        
        self.add_scheduled_task(
            job_func=self.update_list,
            interval='00:00:15',
            name='UpdateList',
        )
        
        self.add_scheduled_task(
            job_func=self.morning,
            interval='06:30',
            name='Morning',
        )
        
        self.add_scheduled_task(
            job_func=self.to_drink,
            interval='14:00',
            name='ToDrink',
        )
        
        self.add_scheduled_task(
            job_func=self.to_bed,
            interval='23:30',
            name='ToBed',
        )
    
    async def update_list(self):
        """ By registering as the job to fetch the friend & group list regularly. """
        group, friend = await asyncio.gather(
            self.api.get_group_list(no_cache=False),
            self.api.get_friend_list(cache=True)
        )
        
        self.list = {
            'group': [group['group_id'] for group in group['data']],
            'friend': [friend['user_id'] for friend in friend['data']]
        }
    
    async def morning(self) -> None:
        """ 固定任务 """
        text = "早上好喵"
        for user_id in self.list['friend']:
            await self.api.post_private_msg(
                user_id=user_id,
                text=text
            )
        for group_id in self.list['group']:
            await self.api.post_group_msg(
                group_id=group_id,
                text=text
            )
    
    async def to_drink(self) -> None:
        """ 固定任务 """
        text = "记得喝水喵"
        for user_id in self.list['friend']:
            await self.api.post_private_msg(
                user_id=user_id,
                text=text
            )
        for group_id in self.list['group']:
            await self.api.post_group_msg(
                group_id=group_id,
                text=text
            )
    
    async def to_bed(self) -> None:
        """ 固定任务 """
        text = "早点睡觉喵"
        for user_id in self.list['friend']:
            await self.api.post_private_msg(
                user_id=user_id,
                text=text
            )
        for group_id in self.list['group']:
            await self.api.post_group_msg(
                group_id=group_id,
                text=text
            )