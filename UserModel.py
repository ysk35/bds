from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from setting import Base
from setting import ENGINE


class User(Base):
  __tablename__ = 'users'
  id = Column('id', Integer, primary_key = True)
  line_user_id = Column('line_user_id', String(200))
  name = Column('name', String(200))
  is_confirm = Column('is_confirm', Boolean)
  is_temporary = Column('is_temporary', Boolean)
  student_number= Column('student_number', String(200))

if __name__ == "__main__":
  # Base.metadata.drop_all(ENGINE)
  Base.metadata.create_all(bind=ENGINE)