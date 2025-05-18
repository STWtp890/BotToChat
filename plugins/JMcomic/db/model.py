from sqlalchemy import Column, String, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Comics(Base):
    __tablename__ = 'comics'

    album_id = Column(String(20), primary_key=True)
    album_name = Column(Text, nullable=False)
    album_author = Column(Text)
    tags = Column(Text)
    pdf_file_path = Column(Text, nullable=False)
    zip_file_path = Column(Text, nullable=False)
