import asyncio

import jmcomic
from jmcomic import JmAlbumDetail, JmModuleConfig, JmDownloader
from ncatbot.core import BotAPI, GroupMessage, PrivateMessage

from ..db import JMcomicDB
from .comic_option import option_construct

text_missing_album = '没有这个漫画喵?'
text_retry_allfail = '请求石沉大海了喵...'
text_request_fail = '请求错误了喵?'
text_jm_err = '发生了模块错误喵...'
text_no_file = '未找到文件喵?'
text_send_fail = '发送失败了喵...'
text_other_err = '发生了未知错误喵...'
text_after_download = "漫画发送啦!"

class SendException(Exception):
    pass


def sync_warp(func):
    """
    A decorator to wrap the async function to sync function.
    """
    
    def wrapper(*args, **kwargs):
        loop = asyncio.get_event_loop()
        return loop.create_task(func(*args, **kwargs))
    
    return wrapper


class JMcomicHandler:
    """ By using jmcomic API to get the comic. """
    
    def __init__(self, api: BotAPI): # Need to pass bot api to the handler.
        self.api = api
        self.db = JMcomicDB()
        self.option = option_construct()
        JmModuleConfig.AFIELD_ADVICE['id'] = lambda album: f'{album.id}'
    
    async def handler(self, album_id: str, msg: PrivateMessage | GroupMessage):
        """ The entry point to handle the message """
        try:
            file_path = await self._get_comic(album_id)
            if file_path is None:
                await self.__comic_download(album_id)
                file_path = self.db.get_comic(album_id)
                if file_path is None:
                    raise FileNotFoundError(f"Get comic has unexceptable error.")
            
            response = await self._send_file(file_path, msg)
            
            if response['status'] != 'ok':
                raise SendException
        
        except jmcomic.MissingAlbumPhotoException:
            await msg.reply(text=text_missing_album)
        except jmcomic.RequestRetryAllFailException:
            await msg.reply(text=text_retry_allfail)
        except jmcomic.ResponseUnexpectedException:
            await msg.reply(text=text_request_fail)
        except FileNotFoundError:
            await msg.reply(text=text_no_file)
        except SendException:
            await msg.reply(text=text_send_fail)
        except jmcomic.JmcomicException:
            await msg.reply(text=text_jm_err)
            raise
        except Exception:
            await msg.reply(text=text_other_err)
            raise
        
        else:
            await self._post_msg(msg)
        
        return None
    
    async def _send_file(self, file_path: str, msg: PrivateMessage | GroupMessage) -> dict | None:
        """ Send the file to the user or group"""
        if isinstance(msg, GroupMessage):
            response = await self.api.post_group_file(group_id=msg.group_id, file=file_path)
        elif isinstance(msg, PrivateMessage):
            response = await self.api.post_private_file(user_id=msg.user_id, file=file_path)
        else:
            raise TypeError('msg must be PrivateMessage or GroupMessage')
        
        if not response or response.get('status') != 'ok':
            raise SendException("Failed to send file, response status is not ok")
        
        return response
    
    async def _post_msg(self, msg: GroupMessage | PrivateMessage) -> None:
        """
        Pack post method, check msg type and use different method.

        :param msg: The incoming message object, can be either a group message or a private message.
        """
        if isinstance(msg, GroupMessage):
            await self.api.post_group_msg(msg.group_id, text=text_after_download)
        elif isinstance(msg, PrivateMessage):
            await self.api.post_private_msg(msg.user_id, text=text_after_download)
        else:
            raise TypeError('msg is not GroupMessage or PrivateMessage')
    
    async def _get_comic(self, album_id) -> str | None:
        """ Check if the comic is already downloaded """
        return self.db.get_comic(album_id)
    
    async def __comic_download(self, album_id: str) -> None:
        """ Handle comic download by callback """
        jmcomic.download_album(
            jm_album_id=album_id,
            option=self.option,
            # Callback will return album & downloader objects.
            callback=self.__comic_db_insert,
        )
    
    def __comic_db_insert(self, album: JmAlbumDetail, downloader: JmDownloader) -> None:
        """	As the midware to insert the comic into the database """
        # DB storage for the comic.
        status = self.db.new_comic(album=album)
        if not status:
            raise ValueError(f'Failed to insert comic: {album.album_id}')