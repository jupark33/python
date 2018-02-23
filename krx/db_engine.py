import os
import sys
import configparser
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Stock_info(Base):
	__tablename__ = 'T_stock_info'
	__table_args__ = {'schema' : 'mss'}
	no = Column(Integer, primary_key=True)
	st_code = Column(String(20), nullable=False)
	st_name = Column(String(50), nullable=False)

class Volume(Base):
	__tablename__ = 'T_volumes'
	__table_args__ = {'schema': 'mss'}
	no = Column(Integer, primary_key=True)
	st_code = Column(String(20), nullable=False)
	volume = Column(Integer, nullable=False)
	dt_date = Column(DateTime, nullable=True)
	dt_time = Column(DateTime, nullable=True)

config = configparser.RawConfigParser()
config.read('db_conn.properties')

id = config.get('connection', 'id')
pw = config.get('connection', 'pw')

print("id : " + id)
print("pw : " + pw)

#engine = create_engine('sqlite:///sqlalchemy_example.db')
url = 'postgresql://' + id + ":" + pw + '@localhost:5432/mss'
engine = create_engine(url)

Base.metadata.create_all(engine)
