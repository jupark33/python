'''
Created on 2018. 3. 4.

@author: pju
'''
import os
import sys
import configparser
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

# btc_krw 비트코인, etc_krw 이더리움 클래식, eth_krw 이더리움, xrp_krw 리플, bch_krw 비트코인 캐시
class Transaction(Base):
    __tablename__ = 'T_coin_transaction'
    __table_args__ = {'schema': 'mcs'}
    no = Column(Integer, primary_key=True)
    tid = Column(Integer, nullable=True)
    price = Column(Integer, nullable=True)
    amount = Column(Float, nullable=True)
    dt_deal = Column(DateTime, nullable=False)
    c_type = Column(Integer, nullable=True)
    
config = configparser.RawConfigParser()
config.read('db_conn.properties')

id = config.get('connection', 'id')
pw = config.get('connection', 'pw')

#engine = create_engine('sqlite:///sqlalchemy_example.db')
url = 'postgresql://' + id + ":" + pw + '@localhost:5432/mcs'
engine = create_engine(url)

Base.metadata.create_all(engine)
