from queue import (
    Queue as Queue,
    Empty as queue_Empty,
)

from threading import (
    Thread as Thread,
)

from jmcomic import (
    JmAlbumDetail, JmModuleConfig, JmDownloader,
    download_album as jmcomic_download_album,
)

from .jmcomic_option import jmcomic_option
from .jmcomic_database import JMComicSQL


class JMComicDownloader:
    def __init__(self, database: JMComicSQL):
        self.database = database
        
        self.jmcomic_option = jmcomic_option
        JmModuleConfig.AFIELD_ADVICE['id'] = lambda album: f'{album.id}'
        
        self.download_tasks_queue = Queue()
        self.consume_thread = Thread(target=self.consume_download_task, daemon=True, name='JMComicDownloader')
        self.consume_thread.start()
        
    def create_download_task(self, album_id: str):
        self.download_tasks_queue.put(album_id)
    
    def consume_download_task(self):
        while True:
            try:
                album_id = self.download_tasks_queue.get(timeout=30)
                self.comic_album_download(album_id)
                self.download_tasks_queue.task_done()
            except queue_Empty:
                continue
    
    def comic_album_download(self, album_id: str):
        jmcomic_download_album(
            jm_album_id=album_id,
            option=jmcomic_option.jm_option,
            callback=self.callback,
        )
        
    def callback(self, album: JmAlbumDetail, downloader: JmDownloader):
        album_authors = ", ".join(album.authors)
        album_tags = ", ".join(album.tags)
        album_dict = {
            'id': album.id,
            'name': album.name,
            'authors': album_authors,
            'tags': album_tags,
        }
        
        self.database.insert_album(album_dict)