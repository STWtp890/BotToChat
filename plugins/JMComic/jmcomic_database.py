from os import path

import sqlalchemy
from sqlalchemy import Column, Text, String
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import declarative_base, sessionmaker

from .jmcomic_path import jmcomic_download_pdf_dir # jmcomic_download_zip_dir
from .jmcomic_config import jmcomic_config_dict


BaseMeta = declarative_base()

class Album(BaseMeta):
    """ Jmcomic Download ORM """
    __tablename__ = "albums"
    
    album_id = Column(String(20), primary_key=True)
    album_name = Column(Text, nullable=False)
    album_author = Column(Text)
    tags = Column(Text)
    pdf_file_path = Column(Text, nullable=False)
    zip_file_path = Column(Text, nullable=True)
    

class JMComicSQL:
    """ MySQL Database Handler """
    def __init__(self):
        self.base_pdf_file_path = jmcomic_download_pdf_dir
        # self.base_zip_file_path = jmcomic_download_zip_dir
        
        self.jmcomic_database = jmcomic_config_dict.get("jmcomic_database")
        self.jmcomic_database_host = jmcomic_config_dict.get("jmcomic_database_host")
        self.jmcomic_database_port = jmcomic_config_dict.get("jmcomic_database_port")
        self.jmcomic_database_username = jmcomic_config_dict.get("jmcomic_database_username")
        self.jmcomic_database_password = jmcomic_config_dict.get("jmcomic_database_password")
        
        self.connection_url = sqlalchemy.engine.URL.create(
            drivername="mysql+pymysql",
            username=self.jmcomic_database_username,
            password=self.jmcomic_database_password,
            host=self.jmcomic_database_host,
            port=self.jmcomic_database_port,
            database=self.jmcomic_database,
        )
        
        self.engine = sqlalchemy.create_engine(self.connection_url, echo=False)
        self.create_albums_table()
        self.Session = sessionmaker(bind=self.engine, autocommit=False, autoflush=False)
        
    def create_albums_table(self) -> None:
        """ Create the albums table """
        Album.metadata.create_all(self.engine)

    def insert_album(self, album: dict) -> None:
        """ Insert a new album into the database """
        pdf_album_file_path = path.join(self.base_pdf_file_path, f"{album.get("id")}.pdf")
        # zip_album_file_path = path.join(self.base_zip_file_path, f"{album.get("id")}.zip")
        
        new_album = Album(
            album_id=album.get("id"),
            album_name=album.get("name"),
            album_author=album.get("authors"),
            tags=album.get("tags"),
            pdf_file_path=pdf_album_file_path,
            # zip_file_path=zip_album_file_path,
        )


        with self.Session() as session:
            try:
                session.add(new_album)
                session.commit()
                session.refresh(new_album)
            except SQLAlchemyError as e:
                session.rollback()
                raise e

    def get_album(self, album_id: str) -> Album:
        """ Get an album from the database """
        with self.Session() as session:
            try:
                select_result = session.execute(
                    sqlalchemy.select(Album).where(Album.album_id == album_id)
                )
                album = select_result.scalars().first()
            except Exception as e:
                raise e

        return album