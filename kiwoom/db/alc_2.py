from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import select

from alc_1 import Base, Stock_info, Volumes, engine

DBSession = sessionmaker(bind=engine)

session = DBSession()

# s = select([T_stock_info])

# for item in session.query(Stock_info).all():
#     print(item)

result = session.query(Stock_info).all()
print(result)

# for info in session.query(Stock_info).all():
#     print(result.no)
