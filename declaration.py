from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
Base = declarative_base()


class Person(Base):
	__tablename__ = 'person'
	id = Column(Integer, primary_key=True, unique=True)
	screen_name = Column(String(250), nullable=False)
	screen_name = Column(String(250), nullable=False)
	description = Column(String(250), nullable=False)
	location = Column(String(250), nullable=False)
	url = Column(String(250))

	followers_count = Column(Integer, default=0)
	statuses_count = Column(Integer, default=0)
	friends_count = Column(Integer, default=0)
	

class Status(Base):
	__tablename__ = 'status'
	id = Column(String(250), primary_key=True, unique=True)
	text = Column(String(250), nullable=False)
	created_at = Column(String(250), nullable=False)
	retweet_count = Column(Integer, default=0)
	retweeted = Column(Boolean, default=False)

	person_id = Column(Integer, ForeignKey('person.id'))
	person =  relationship('person')



engine = create_engine('sqlite:///twittet_app.db')

Base.metadata.create_all(engine)


#============================================	
