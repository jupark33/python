import os
import sys
import datetime
import ConfigParser
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Stock_info(Base):
	__tablename__ = 'T_stock_info'
	no = Column(Integer, primary_key=True)
	st_code = Column(String(20), nullable=False)
	st_name = Column(String(50), nullable=False)

class Volumes(Base):
	__tablename__ = 'T_volumes'
	no = Column(Integer, primary_key=True)
	st_code = Column(String(20), nullable=False)
	volume = Column(Integer, nullable=False)
	dt_date = Column(Datetime)
	dt_time = Column(Datetime)

config = ConfigParser.RawConfigParser()
config.read('db_conn.properties')

id = config.get('connection', 'id')
pw = config.get('connection', 'pw')

#engine = create_engine('sqlite:///sqlalchemy_example.db')
url = 'postgresql://' + id + ":" + pw + '@localhost:5432/mms'
engine = create_engine(url)

Base.metadata.create_all(engine)
