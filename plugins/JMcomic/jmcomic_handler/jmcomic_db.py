import sqlite3
from os import path

from jmcomic import JmAlbumDetail

from ..path import (
	jmcomic_base_dir,
	jmcomic_download_pdf_dir,
	jmcomic_download_zip_dir
)


class JMcomicDB:
	""" SQLite3 database handler for JMcomic. """
	
	def __init__(self):
		comic_db_path = jmcomic_base_dir.replace('/', '\\') + '\\jmcomic.db'
		self.conn = sqlite3.connect(comic_db_path)
		if not self._comic_table_exists():
			self._create_comic_table()
	
	async def get_comic(self, album_id: str) -> str:
		with self.conn as conn:
			cursor = conn.execute(
				"SELECT pdf_file_path FROM comics WHERE album_id = ?;",
				(album_id,))
			res = cursor.fetchone()
			return res[0] if res else None
	
	def new_comic(self, album: JmAlbumDetail):
		authors = ','.join(album.authors)
		tags = ','.join(album.tags)
		pdf_file_path = self.set_file_path(file_name=album.album_id, file_type='pdf')
		zip_file_path = self.set_file_path(file_name=album.album_id, file_type='zip')
		
		if not pdf_file_path or not zip_file_path:
			raise ValueError(f'Invalid file path: {pdf_file_path} or {zip_file_path}')
		
		with self.conn as conn:
			conn.execute(
				"INSERT INTO comics ("
				"album_id, album_name, album_author, tags, pdf_file_path, zip_file_path"
				") VALUES (?, ?, ?, ?, ?, ?);",
				(album.album_id, album.name, authors, tags, pdf_file_path, zip_file_path)
			)
			conn.commit()
		
		return True
	
	def _comic_table_exists(self):
		with self.conn as conn:
			cursor = conn.execute(
				"SELECT name FROM sqlite_master WHERE type='table' AND name='comics';"
			)
			res = cursor.fetchone()
			return True if res else False
	
	def _create_comic_table(self):
		with self.conn as conn:
			conn.execute(
				"CREATE TABLE IF NOT EXISTS comics ("
				"    album_id VARCHAR(20) PRIMARY KEY,"
				"    album_name TEXT NOT NULL,"
				"    album_author TEXT,"
				"    tags TEXT,"
				"    pdf_file_path TEXT NOT NULL,"
				"    zip_file_path TEXT NOT NULL"
				");"
			)
			conn.commit()
	
	@staticmethod
	def set_file_path(file_name: str, file_type: str, set_dir: str | None = None) -> str:
		if not set_dir:
			if file_type == 'pdf':
				dir = path.join(
					jmcomic_download_pdf_dir,
					file_name + f'.{file_type}'
				)
			elif file_type == 'zip':
				dir = path.join(
					jmcomic_download_zip_dir,
					file_name + f'.{file_type}'
				)
			else:
				raise ValueError(f'Invalid file type: {file_type}')
		else:
			dir = path.join(
				set_dir,
				file_name + f'.{file_type}'
			)
		
		return dir
