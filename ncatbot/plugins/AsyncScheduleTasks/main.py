import asyncio

from apscheduler.executors.pool import ThreadPoolExecutor
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from ncatbot.core import GroupMessage, PrivateMessage
from ncatbot.plugin import BasePlugin, CompatibleEnrollment

from .path import AST_base_dir
from .scheduler.utils import slice_raw_msg

bot = CompatibleEnrollment


# TODO: Test the plugin.
# TODO: Add mail-sending remind ability for the plugin.

class APS(BasePlugin):
	"""
	- An asynchronous scheduling plugin for NcatBot.
	- This plugin uses APScheduler to instead of the Ncatbot original scheduling plugin.
	"""
	
	name = "AsyncScheduleTasks"
	version = '0.1.0'
	dependencies = {}
	description = "AsyncScheduleTasks"
	
	async def on_load(self) -> None:
		""" - Init the scheduler & Register the regular job. """
		self.loop = asyncio.get_event_loop()
		# Init the scheduler.
		self.scheduler = AsyncIOScheduler(
			job_stores={
				'default': SQLAlchemyJobStore(url=f"sqlite:///{AST_base_dir}/schedule.db"),
			},
			executors={
				'default': ThreadPoolExecutor(10),
				'processpool': ThreadPoolExecutor(10),
			},
			job_defaults={
				'coalesce': True,
				'max_instances': 3,
			},
			timezone="Asia/Shanghai",
		)
		await self.update_list()
		self.scheduler.start()
		
		# Register the regular job.
		self.scheduler.add_job(  # Update the friend & group list.
			func=self.update_list,
			trigger=CronTrigger(
				hour=0,
				minute=0
			),
			max_instances1=1,
			misfire_grace_time=3600,
			coalesce=True,
			name="update_list",
		)
		
		self.scheduler.add_job(  # Drink remind.
			func=self.to_drink,
			trigger=CronTrigger(
				hour=14,
				minute=30
			),
			max_instances1=1,
			misfire_grace_time=3600,
			coalesce=True,
			name="to_drink",
		)
	
	@bot.group_event(types="all")
	async def on_group_message(self, msg: GroupMessage) -> None:
		self.loop.create_task(self.on_msg(msg))
	
	@bot.private_event(types="all")
	async def on_private_message(self, msg: PrivateMessage) -> None:
		self.loop.create_task(self.on_msg(msg))
	
	async def on_msg(self, msg: GroupMessage | PrivateMessage) -> None:
		""" - Check if the message is a command. """
		if not msg.raw_message.startwith("/"):
			return None
		if msg.raw_message.startswith("/aps"):
			return None
		if msg.raw_message.startswith("/aps help"):
			if msg.group_id:
				await self.api.post_group_msg(msg.group_id, text=await self.help())
			else:
				await self.api.post_private_msg(msg.user_id, text=await self.help())
			return None
		if msg.raw_message.find("-g") and type(msg) == PrivateMessage:
			await msg.reply("定时任务参数错误, 请检查参数格式")
			return None
		
		await self.add_user_job(msg)
		
		return None
	
	async def add_user_job(self, msg: GroupMessage | PrivateMessage) -> None:
		""" - Add a custom user job. """
		msg_params = await slice_raw_msg(msg.raw_message)
		if not msg_params or not msg_params['c']:
			await msg.reply("定时任务参数错误, 请检查参数格式")
			return None
		
		msg_params['group_id'] = msg.group_id if msg.group_id else None
		msg_params['user_id'] = msg.user_id if msg.user_id else None
		try:
			self.scheduler.add_job(
				func=self.to_drink,
				kwargs=msg_params,
				trigger=CronTrigger(**msg_params['c']),
				max_instances1=1,
				misfire_grace_time=3600,
				coalesce=True,
				name=f"{msg_params['n']}",
			)
		except TypeError as t:
			await msg.reply("定时任务参数错误, 请检查参数格式")
		except ValueError as v:
			await msg.reply("定时任务参数错误, 请检查参数格式")
		except Exception as e:
			await msg.reply("定时任务注册失败")
			raise e
		else:
			if msg_params['g']:
				await self.api.post_group_msg(msg.group_id, f"已添加群定时任务:{msg_params['n']}", reply=msg.message_id)
			else:
				await self.api.post_private_msg(msg.user_id, f"已添加定时任务:{msg_params['n']}", reply=msg.message_id)
		
		return None
	
	async def custom_job(self, **kwargs) -> None:
		"""
		- Custom job function.
		- This function will be called when the job is triggered.
		"""
		if kwargs['g']:
			await self.api.post_group_msg(
				group_id=kwargs['group_id'],
				text=f"定时任务: {kwargs['n']}"
				     f"{kwargs['t']}"
			)
		else:
			await self.api.post_private_msg(
				user_id=kwargs['user_id'],
				text=f"定时任务: {kwargs['n']}"
				     f"{kwargs['t']}"
			)
		
		return None
	
	async def help(self):
		"""
		- To get AST plugin help to use.
		:return: Help info string.
		"""
		return f"""
		#AST帮助:
		/ast
		-n [任务名]
		-t [任务信息]
		-c re:[cron格式的定时参数]
		-g [True | Fasle]
		#cron基本格式例:
		"re:year=?month=?day=?hour=?minute=?second=?week=?dowek=?start=?end=?"
		其中start,date 形式应符合引号内"%Y/%m/%d %H:%M"格式.
		推荐使用cron在线生成.
		"""
	
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
	
	async def to_drink(self) -> None:
		""" 固定任务 """
		for user_id, group_id in self.list['group'], self.list['friend']:
			await asyncio.gather(
				self.api.post_group_msg(
					group_id=group_id,
					text="喝水时间到, 请喝水"
				),
				self.api.post_private_msg(
					user_id=user_id,
					text="喝水时间到, 请喝水"
				)
			)
	
	async def to_bed(self) -> None:
		""" 固定任务 """
		for user_id, group_id in self.list['group'], self.list['friend']:
			await asyncio.gather(
				self.api.post_group_msg(
					group_id=group_id,
					text="晚安, 祝你做个好梦"
				),
				self.api.post_private_msg(
					user_id=user_id,
					text="晚安, 祝你做个好梦"
				)
			)
