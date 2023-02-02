# Add table related data to the ORM
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class MailTrack(Base):
    __tablename__ = 'mail_track'
    id = Column(Integer, primary_key=True)
    mail_id = Column(String(250), nullable=False)
    time = Column(DateTime, nullable=False)
