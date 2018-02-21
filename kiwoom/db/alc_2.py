from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from alc_1 import Base, Stock_info, Volumes, engine

DBSession = sessionmaker(bind=engine)

session = DBSession()


