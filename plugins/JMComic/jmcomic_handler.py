import asyncio

from .jmcomic_database import JMComicSQL
from .jmcomic_downloader import JMComicDownloader


class JMcomicHandler:
    """ By using jmcomic API to crawl comics. """
    
    def __init__(self, event_loop: asyncio.AbstractEventLoop):
        self.event_loop = event_loop
        self.database = JMComicSQL()
        self.downloader = JMComicDownloader(self.database)
        
    async def find(self, album_id: str) -> dict | None:
        return await self.comic_handler(album_id)
    
    async def comic_handler(self, album_id: str) -> dict | None:
        """ The entry point to handle the message """
        if not self.album_exist(album_id):
            self.create_comic_task(album_id)
        return await self.get_album(album_id)
    
    def album_exist(self, album_id: str) -> bool:
        """ Check if the album exists in database """
        return True if self.database.get_album(album_id) else False
    
    def create_comic_task(self, album_id: str) -> None:
        """ Put album id to downloader task queue """
        self.downloader.create_download_task(album_id)
    
    async def get_album(self, album_id: str) -> dict | None:
        """
        Get the comic storage attributes from database
        """
        album = None
        wait_time = 0
        while not album and wait_time < 12:
            try:
                wait_time += 1
                await asyncio.sleep(10)
                album = self.database.get_album(album_id)
            except Exception as e:
                raise e
        
        if not album:
            return None
        
        album_dict = {
            "album_id": album.album_id,
            "album_name": album.album_name,
            "album_author": album.album_author,
            "album_tags": album.tags,
            "pdf_file_path": album.pdf_file_path,
            "zip_file_path": album.zip_file_path
        }
        return album_dict