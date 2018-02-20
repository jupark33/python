import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Stock_info(Base):
	__tablename__ = 'T_stock_info'
	no = Column(Integer, primary_key=True)
	st_code = Column(String(20), nullable=False)
