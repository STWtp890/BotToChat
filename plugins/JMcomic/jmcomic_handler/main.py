import jmcomic
from jmcomic import JmAlbumDetail, JmModuleConfig, JmDownloader
from ncatbot.core import BotAPI, GroupMessage

from .jmcomic_db import JMcomicDB
from .jmcomic_option import option_construct


class SendException(Exception):
	pass


class JMcomicHandler:
	""" By using jmcomic API to get the comic. """
	
	def __init__(self, api: BotAPI):
		self.api = api
		self.db = JMcomicDB()
		self.option = option_construct()
		JmModuleConfig.AFIELD_ADVICE['id'] = lambda album: f'{album.id}'
	
	async def handler(self, album_id: str, msg: GroupMessage):
		""" The entry point to handle the message """
		try:
			file = await self.db.get_comic(album_id)
			if file is not None:
				await self.api.post_private_file(user_id=msg.user_id, file=file)
			else:
				self.comic_download(album_id)
				file_path = await self.db.get_comic(album_id)
				if file_path is None:
					raise FileNotFoundError
				response = await self.api.post_private_file(user_id=msg.user_id, file=file_path)
				if response['status'] != 'ok':
					raise SendException
		except jmcomic.MissingAlbumPhotoException:
			await msg.reply(text='漫画似乎没有喵?')
		except jmcomic.RequestRetryAllFailException:
			await msg.reply(text='试了几次石沉大海了喵...')
		except jmcomic.JmcomicException or FileNotFoundError:
			await msg.reply(text='发生了未知错误喵...')
		except SendException:
			await msg.reply(text='漫画发送失败了喵?')
		except Exception as err:
			await msg.reply(text='发生了未知错误喵...')
			raise err
		else:
			await self.api.post_group_msg(msg.group_id, text='漫画发送请查收喵!')
		return None
	
	async def get_comic(self, album_id):
		""" check if the comic is already downloaded """
		return self.db.get_comic(album_id)
	
	def comic_download(self, album_id: str):
		""" Handle comic download by callback """
		# JM下载 与 回调
		jmcomic.download_album(
			jm_album_id=album_id,
			option=self.option,
			# callback会传递album与downloader对象
			callback=self.comic_db_insert,
		)
	
	def comic_db_insert(self, album: JmAlbumDetail, downloader: JmDownloader) -> None:
		"""	As the midware to insert the comic into the database """
		# 存储管理
		status = self.db.new_comic(album=album)
		if status != True:
			raise ValueError(f'Failed to insert comic: {album.album_id}')
