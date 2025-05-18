import os

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, select

from jmcomic import JmAlbumDetail

from .model import Comics
from ..path import (
    jmcomic_database_path,
    jmcomic_download_pdf_dir,
    jmcomic_download_zip_dir
)

class JMcomicDB:
    """ Sync SQLite3 database handler """

    def __init__(self):
        # Contribute database url
        db_path = jmcomic_database_path
        db_url = f"sqlite:///{db_path}/comics.db"
        
        # Create sync engine
        self.engine = create_engine(db_url, echo=False)

        # Initialize database
        self._initialize_db()
        
        # Create sync session
        self.Session = sessionmaker(
            bind=self.engine, autocommit=False, autoflush=False
        )

    def _initialize_db(self):
        Comics.metadata.create_all(self.engine)
        
    def get_comic(self, album_id: str) -> str | None:
        with self.Session() as session:
            result = session.execute(
                select(Comics.pdf_file_path).where(Comics.album_id == album_id)
            )
            row = result.fetchone()
            return row[0] if row else None

    def new_comic(self, album: JmAlbumDetail) -> bool:
        authors = ','.join(album.authors)
        tags = ','.join(album.tags)
        pdf_file_path = self.generate_file_path(file_name=album.album_id, file_type='pdf')
        zip_file_path = self.generate_file_path(file_name=album.album_id, file_type='zip')

        if not pdf_file_path or not zip_file_path:
            raise ValueError(f'Invalid file path: {pdf_file_path} or {zip_file_path}')

        try:
            with self.Session() as session:
                with session.begin():
                    comic = Comics(
                        album_id=album.album_id,
                        album_name=album.name,
                        album_author=authors,
                        tags=tags,
                        pdf_file_path=pdf_file_path,
                        zip_file_path=zip_file_path
                    )
                    session.add(comic)
            return True
        except Exception as e:
            print(f"Database error: {e}")
            return False

    @staticmethod
    def generate_file_path(file_name: str, file_type: str, set_dir: str | None = None) -> str:
        if not set_dir:
            if file_type == 'pdf':
                dir_path = os.path.join(
                    jmcomic_download_pdf_dir,
                    file_name + f'.{file_type}'
                )
            elif file_type == 'zip':
                dir_path = os.path.join(
                    jmcomic_download_zip_dir,
                    file_name + f'.{file_type}'
                )
            else:
                raise ValueError(f'Invalid file type: {file_type}')
        else:
            dir_path = os.path.join(
                set_dir,
                file_name + f'.{file_type}'
            )

        return dir_path